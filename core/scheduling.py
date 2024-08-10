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

    task, created = PeriodicTask.objects.update_or_create(
        name='Scrape Berhan',
        defaults={
            'interval': schedule,
            'task': 'core.tasks.scrape_berhan',
        }
    )

    task, created = PeriodicTask.objects.update_or_create(
        name='Scrape Dashen',
        defaults={
            'interval': schedule,
            'task': 'core.tasks.scrape_dashen',
        }
    )

    task, created = PeriodicTask.objects.update_or_create(
        name='Scrape Nib',
        defaults={
            'interval': schedule,
            'task': 'core.tasks.scrape_nib',
        }
    )

    task, created = PeriodicTask.objects.update_or_create(
        name='Scrape Tsedey',
        defaults={
            'interval': schedule,
            'task': 'core.tasks.scrape_tsedey',
        }
    )