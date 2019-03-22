from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
import core.views as views

app_name = 'core'

router = DefaultRouter()
router.register('users', views.UserViewSet, base_name='users')

urlpatterns = [
    path('users/login/', views.LoginView.as_view(), name="login"),
]

urlpatterns += router.urls

