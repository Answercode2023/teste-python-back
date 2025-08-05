from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, RegisterView,TaskFilteredListView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterView.as_view(), name='register'),
#    path('tasks/filter/', TaskFilteredListView.as_view(), name='task-filter'),
path('tasks-filtrar/', TaskFilteredListView.as_view(), name='task-filtrar'),
]
