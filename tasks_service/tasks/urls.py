from django.urls import path
from . import views

urlpatterns = [
    path("summarize/", views.TaskList.as_view())
]