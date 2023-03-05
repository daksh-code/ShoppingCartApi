from django.urls import path
from authentication.views import  LoginView

urlpatterns = [
    #path('login/', LoginView.as_view()),
     path('login/', LoginView.as_view()),
]
