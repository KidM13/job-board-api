from celery import shared_task

@shared_task
def notify_recruiter(application_id):
    from .models import Application
    application = Application.objects.get(id=application_id)
    print(f"New application from {application.user.username} for job: {application.job.title}")