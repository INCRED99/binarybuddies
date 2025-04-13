from django.urls import path
from . import views
print("DEBUG: Imported views module:", views)  # Debugging

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('home/', views.home_page, name='home'),
    path('stats/', views.stats_page, name='stats'),
    path('predict/', views.predict, name='predict'),
    path('reset/', views.reset_data, name='reset_data'),  # ✅ Reset URL
    path('chatbot/', views.chatbot, name='chatbot'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('community/', views.community_page, name='community'),
    #path('pole/', views.pole_page, name='pole'),
]
