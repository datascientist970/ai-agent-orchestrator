from django.shortcuts import render
from django.views import View
from .models import Task, AgentStep, Memory
from .agent_graph import planner, worker, evaluator
from .memory import query_vectors
import re
import traceback
from django.http import HttpResponseServerError

class RunAgentView(View):
    template_name = "index.html"
    error_template = "quota_exceeded.html"
    generic_error_template = "error/generic.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_input = request.POST.get("user_input")
        
        if not user_input:
            return render(request, self.template_name, {
                'error': 'Please enter a task'
            })

        try:
            # --- Step 1: Create Task ---
            task = Task.objects.create(user_input=user_input)

            # --- Step 2: Initialize state ---
            state = {"input": user_input}

            # --- Step 3: Planner Agent ---
            try:
                state = planner(state)
            except Exception as e:
                # Handle planner-specific errors
                task.status = "failed"
                task.error_message = f"Planner agent failed: {str(e)}"
                task.save()
                raise  # Re-raise to be caught by outer try block

            AgentStep.objects.create(
                task=task,
                agent_name="Planner",
                input_data=user_input,
                output_data=state.get("plan", "No plan generated")
            )

            # --- Step 4: Worker Agent ---
            try:
                # Include context from memory
                context = "\n".join(query_vectors(user_input))
                state["plan_with_context"] = f"{state['plan']}\nContext:\n{context}"
                state = worker(state)
            except Exception as e:
                task.status = "failed"
                task.error_message = f"Worker agent failed: {str(e)}"
                task.save()
                raise

            AgentStep.objects.create(
                task=task,
                agent_name="Worker",
                input_data=state.get("plan_with_context", "No context"),
                output_data=state.get("result", "No result generated")
            )

            # --- Step 5: Evaluator Agent ---
            try:
                state = evaluator(state)
            except Exception as e:
                task.status = "failed"
                task.error_message = f"Evaluator agent failed: {str(e)}"
                task.save()
                raise

            AgentStep.objects.create(
                task=task,
                agent_name="Evaluator",
                input_data=state.get("result", "No result"),
                output_data=state.get("evaluation", "No evaluation generated")
            )

            # --- Step 6: Save final output ---
            task.final_output = state.get("result", "No final output generated")
            task.status = "completed"
            task.save()

            # --- Step 7: Get all agent steps for display ---
            agent_steps = task.steps.all().order_by("created_at")

            context = {
                "task": task,
                "agent_steps": agent_steps,
                "user_input": user_input,
                "success": True
            }
            return render(request, self.template_name, context)

        except Exception as e:
            error_str = str(e)
            error_lower = error_str.lower()
            
            # Print for debugging (optional - remove in production)
            import traceback
            traceback.print_exc()
            
            # Check if it's a quota exceeded error (Gemini API)
            if any(term in error_lower for term in [
                'quota exceeded', 
                '429', 
                'resource_exhausted', 
                'rate limit',
                'generate_content_free_tier_requests',
                'retry in'
            ]):
                # Extract retry time if available
                retry_time = 60  # Default 60 seconds
                
                # Try to extract retry time from error message
                time_match = re.search(r'retry in ([\d.]+)s', error_lower)
                if not time_match:
                    time_match = re.search(r'please retry in ([\d.]+)s', error_lower)
                if not time_match:
                    time_match = re.search(r'after ([\d.]+) seconds', error_lower)
                
                if time_match:
                    retry_time = float(time_match.group(1))
                
                # Extract model name if available
                model_name = 'gemini-2.5-flash'  # Default
                model_match = re.search(r'model: ([\w.-]+)', error_str)
                if model_match:
                    model_name = model_match.group(1)
                
                # Extract quota limit if available
                quota_limit = 20  # Default
                limit_match = re.search(r'limit: (\d+)', error_lower)
                if limit_match:
                    quota_limit = limit_match.group(1)
                
                # Render quota exceeded page with retry time
                return render(request, self.error_template, {
                    'retry_seconds': retry_time,
                    'error_details': error_str,
                    'model_name': model_name,
                    'quota_limit': quota_limit,
                    'error_code': '429'
                }, status=429)
            
            else:
                # Handle other errors (database, network, etc.)
                error_type = type(e).__name__
                
                # Check if task was created
                if 'task' in locals():
                    task.status = "failed"
                    task.error_message = f"{error_type}: {error_str[:500]}"  # Limit length
                    task.save()
                
                return render(request, self.generic_error_template, {
                    'error': error_str,
                    'error_type': error_type,
                    'user_input': user_input
                }, status=500)


# Optional: Add a health check view
def health_check(request):
    """Simple health check endpoint"""
    from django.http import JsonResponse
    return JsonResponse({"status": "healthy", "message": "Agentic AI system is running"})


# Optional: Test view for quota error page (remove in production)
def test_quota_error(request):
    """Test view to preview the quota error page"""
    return render(request, "error/quota_exceeded.html", {
        'retry_seconds': 46.69,
        'model_name': 'gemini-2.5-flash',
        'quota_limit': 20,
        'error_details': 'Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20'
    })


# Optional: Clear failed tasks (admin utility)
def clear_failed_tasks(request):
    """Clear all failed tasks (for debugging)"""
    if request.user.is_staff:  # Only staff can do this
        failed_tasks = Task.objects.filter(status='failed')
        count = failed_tasks.count()
        failed_tasks.delete()
        from django.http import JsonResponse
        return JsonResponse({"message": f"Cleared {count} failed tasks"})
    else:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()