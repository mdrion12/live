from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)   
    def __str__(self):
        return self.username


# Create your models here.
class Match(models.Model):
    id = models.AutoField(primary_key=True)  # কমা সরানো
    first_team = models.CharField(max_length=100)
    second_team = models.CharField(max_length=100)
    match_time = models.DateTimeField()
    first_team_image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    second_team_image = models.ImageField(upload_to='team_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_team} vs {self.second_team} at {self.match_time}"
class Over(models.Model):
    over_number = models.IntegerField()  # কমা সরানো

    def __str__(self):
        return f"Over {self.over_number}"


class Batting(models.Model):
    id = models.AutoField(primary_key=True)  # কমা সরানো
    batsman_name = models.CharField(max_length=100)
    runs_scored = models.IntegerField()
    balls_faced = models.IntegerField()
    in_at = models.IntegerField()

    def __str__(self):
        return f"Batsman: {self.batsman_name}, Runs: {self.runs_scored}, Balls: {self.balls_faced}" 


class Extra(models.Model):
    extra_runs = models.IntegerField()  # কমা সরানো

    def __str__(self):
        return f"Extra Runs: {self.extra_runs}"
