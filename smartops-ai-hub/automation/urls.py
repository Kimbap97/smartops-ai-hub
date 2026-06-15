from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_index, name='dashboard'),
    path('api/process/', views.process_automation_api, name='process_api'),
]
