from celery import Celery
from app import create_app
from application.jobs import reminder, send_mail
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        broker = 'redis://localhost:6379/0', backend = 'redis://localhost:6379/1',
        timezone='Asia/Kolkata',
        broker_connection_retry_on_startup=True,
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

flask_app = create_app()
celery_app = make_celery(flask_app)

# daily remainder
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #     crontab(minute='*'),
    #     reminder.s()
    # )
    sender.add_periodic_task(
        crontab(hour=10, minute=10),
        reminder.s()
    )

# monthly report
@celery_app.on_after_configure.connect
def setup_email(sender, **kwargs):
    # sender.add_periodic_task(
    #     crontab(minute='*'),
    #     send_mail.s()
    # )
    sender.add_periodic_task(
        crontab(day_of_month='13', hour=10, minute=12),
        send_mail.s()
    )
    
