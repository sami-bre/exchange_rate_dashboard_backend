from django_celery_beat.models import PeriodicTask, IntervalSchedule

def setup_periodic_tasks():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=2,
        period=IntervalSchedule.MINUTES,
    )
    
    task, created = PeriodicTask.objects.update_or_create(
        name='Scrape BOA',
        defaults={
            'interval': schedule,
            'task': 'core.tasks.scrape_boa',
        }
    )