

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
class SearchBar(models.Model):
    search=models.CharField(max_length=250)
    def _str_(self):
        return self.search
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user_email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # To track if the notification has been read

    def __str__(self):
        return f'Notification for {self.user_email} - {self.message}'