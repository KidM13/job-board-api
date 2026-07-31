from django.db import models
from django.conf import settings

# Create your models here.
class Company(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    website=models.URLField()
    recruiter=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


