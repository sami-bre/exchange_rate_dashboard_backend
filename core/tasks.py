from celery import shared_task

@shared_task
def sample_task():
    print("Hello from Celery!")
    return "Hello from Celery!"