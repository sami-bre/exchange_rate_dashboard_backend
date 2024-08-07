from django_celery_beat.models import PeriodicTask, IntervalSchedule

def setup_periodic_tasks():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
    
    task, created = PeriodicTask.objects.update_or_create(
        name='Fetch exchange rates',
        defaults={
            'interval': schedule,
            'task': 'core.tasks.sample_task',
        }
    )