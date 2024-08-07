from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .scheduling import setup_periodic_tasks
        # Connect the setup_periodic_tasks to the post_migrate signal
        post_migrate.connect(setup_periodic_tasks_wrapper, sender=self)

@receiver(post_migrate)
def setup_periodic_tasks_wrapper(sender, **kwargs):
    from .scheduling import setup_periodic_tasks
    setup_periodic_tasks()
