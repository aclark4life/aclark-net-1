from django.core.management.base import BaseCommand, CommandError
from aclark.db.models import Project
from aclark.db.mail import get_recipients
from aclark.db.mail import mail_send


class Command(BaseCommand):
    """
    """

    help = "Notify project team members"

    def handle(self, *args, **options):
        projects = Project.objects.filter(active=True)
        for project in projects:
            recipients = get_recipients(project)
            for recipient in recipients:
                first_name = recipient[0]
                email_address = recipient[1]
                notifications = recipient[2]
                email_message = "Test"
                email_subject = "Test"
                if notifications:
                    mail_send(message=email_message, subject=email_subject)
                    self.stdout.write(
                        self.style.SUCCESS("Successfully notified: %s" % recipient[0])
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS("Skipped notifying: %s" % recipient[0])
                    )
        self.stdout.write(self.style.SUCCESS("Done."))
