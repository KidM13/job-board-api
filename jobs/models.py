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
class Job(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    title=models.CharField(max_length=250)
    description=models.TextField()
    location=models.CharField(max_length=250)
    salary_min=models.DecimalField(max_digits=10, decimal_places=2)
    salary_max=models.DecimalField(max_digits=10, decimal_places=2)
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('remote', 'Remote'),
    ]
    
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    is_active=models.BooleanField()
    deadline=models.DateField()
    def __str__(self):
        return self.title
