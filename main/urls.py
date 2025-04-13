from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('home/', views.home_page, name='home'),
    path('stats/', views.stats_page, name='stats'),
    path('predict/', views.predict, name='predict'),  # ✅ This is correct
    path('chatbot/', views.chatbot, name='chatbot'),  # ✅ Chatbot route
]

