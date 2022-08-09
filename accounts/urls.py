from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path("login/", LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CreateView.as_view(
        template_name = 'signup.html',
        form_class = UserCreationForm,
        success_url = '/'
    ), name='signup'),
]