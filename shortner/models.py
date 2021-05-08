from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class shortUrl(models.Model):
    original_url = models.URLField(blank=False)
    short_url = models.CharField(max_length=8, blank=False)
    visits = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
