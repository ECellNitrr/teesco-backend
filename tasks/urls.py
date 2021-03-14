from django.urls import path
from .views import TaskView

urlpatterns = [
    path('org/<int:org_id>', TaskView.as_view(), name='create_task'),
    path('org/<int:org_id>', TaskView.as_view(), name='get_task'),
]
