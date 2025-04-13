from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),  # This will serve the landing page
    path('home/', views.home_page, name='home'),   # This will serve the home page
    path('stats/', views.stats_page, name='stats'),   # This will serve the home page
    path('chatbot/', views.chatbot, name='chatbot'),  # Add this line to handle the chatbot endpoint
    path('predict/', views.predict, name='predict'),
]
