from django.core.mail import send_mail
from django_cron import CronJobBase, Schedule
from .models import Event
from datetime import datetime

# Send email notifications.
class SendNotificationCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Check every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'event_api.send_notification'  # Unique code

    def do(self):
        events = Event.objects.filter(date_time__date=datetime.date.today())
        for event in events:
            for user in event.registered_users.all():
                send_mail(
                    f"Reminder for {event.title}",
                    f"The event {event.title} is happening soon.",
                    'from@example.com',
                    [user.email],
                )
