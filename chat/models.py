from django.db import models
from django.contrib.auth.models import User

class WordPair(models.Model):
    first_word = models.CharField(max_length=100)
    second_word = models.CharField(max_length=100)
    frequency = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.first_word} -> {self.second_word}"

class DailyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    reminder_time = models.TimeField()  # e.g., 08:00:00
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.task_name} at {self.reminder_time}"
    

class Knowledge(models.Model):
    keyword = models.CharField(max_length=100, unique=True)
    # Using a TextField to store multiple responses separated by a | character
    responses = models.TextField(help_text="Separate multiple responses with |")

    def get_random_response(self):
        import random
        return random.choice(self.responses.split('|'))


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    user_message = models.TextField()
    paksiw_response = models.TextField(blank=True, null=True)
    is_manual_reply = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat ni {self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"