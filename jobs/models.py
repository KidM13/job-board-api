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
class Application(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_at=models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    class Meta:
        unique_together = ['user', 'job']
    def __str__(self):
        return f"{self.user} applied for a job {self.Job}"

