from django.db import models
import uuid

# --------------------------
# Task submitted by user
# --------------------------
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_input = models.TextField(help_text="User's task or goal")
    status = models.CharField(
        max_length=50, default="pending", help_text="Task status: pending, completed"
    )
    final_output = models.TextField(null=True, blank=True, help_text="Final AI output")
    confidence = models.FloatField(
        null=True, blank=True, help_text="Optional confidence score from evaluator"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.id} - {self.status}"


# --------------------------
# Steps executed by agents
# --------------------------
class AgentStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="steps")
    agent_name = models.CharField(max_length=100, help_text="Planner / Worker / Evaluator")
    input_data = models.TextField(help_text="Input given to this agent")
    output_data = models.TextField(help_text="Output returned by this agent")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent_name} step for Task {self.task.id}"


# --------------------------
# Optional: Embedding Memory Table
# --------------------------
class Memory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(help_text="Original text stored in memory")
    vector_id = models.CharField(max_length=255, help_text="ID in vector database")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Memory {self.vector_id}"
