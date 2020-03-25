from django.urls import path
from django.contrib.auth.views import LoginView
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('signup/', views.SingUpView.as_view(), name='signup')
]