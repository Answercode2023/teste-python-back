from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, RegisterView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterView.as_view(), name='register'),
]
