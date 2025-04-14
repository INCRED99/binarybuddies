from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone





class Footprint(models.Model):
    electricity = models.FloatField()
    car_km = models.FloatField()
    meat_meals = models.FloatField()
    flights = models.FloatField()
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Footprint on {self.timestamp} - Score: {self.score}"



class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, choices=[('motivational', 'Motivational'), ('fact', 'Fact'), ('warning', 'Warning')], default='fact')

    def __str__(self):
        return f"{self.text} — {self.author if self.author else 'Unknown'}"
    
class UserScore(models.Model):
    username = models.CharField(max_length=100)
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    # Streak tracking
    last_visit = models.DateField(null=True, blank=True)
    streak_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} - {self.score}/{self.total} (Streak: {self.streak_count})"
    

class Streak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_visited = models.DateField(default=timezone.now)
    streak_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.streak_count} days"    
    


    