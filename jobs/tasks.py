from celery import shared_task

@shared_task
def notify_recruiter(application_id):
    from .models import Application
    application = Application.objects.get(id=application_id)
    print(f"New application from {application.user.username} for job: {application.job.title}")

@shared_task
def deactivate_expired_jobs():
    from django.utils import timezone
    from .models import Job
    jobs=Job.objects.filter(is_active=True,deadline__lt=timezone.now.date())
    for job in jobs:
        job.is_active=False
        job.save()

        
    
        

   