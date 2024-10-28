from django.urls import path
from authentification.views import views

urlpatterns = [
    path('/signup', views.RegisterView.as_view(), name='signup'),
    path('/signin', views.LoginView.as_view(), name='signin'),
    path('/profile', views.ProfileView.as_view(), name='profile'),
]