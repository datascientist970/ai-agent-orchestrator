from django.urls import path
from . import views

urlpatterns = [
    path('', views.RunAgentView.as_view(), name='home'),
    path('health/', views.health_check, name='health_check'),
    
    # Remove these in production - for testing only
    path('test-quota-error/', views.test_quota_error, name='test_quota_error'),
    
    # Optional admin utility
    path('admin/clear-failed/', views.clear_failed_tasks, name='clear_failed_tasks'),
]