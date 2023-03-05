from django.urls import path
from authentication.views import  LoginView
from authentication.views import RegistrationView

urlpatterns = [
    #path('login/', LoginView.as_view()),
     path('login/', LoginView.as_view()),
     path('registration/', RegistrationView.as_view()),
]
