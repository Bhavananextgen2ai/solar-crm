# leads/management/commands/send_followup_reminders.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from leads.models import Lead
from django.conf import settings


class Command(BaseCommand):
    help = 'Send email reminders for today follow-ups'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        leads = Lead.objects.filter(
            follow_up_date=today
        )

        if not leads.exists():
            self.stdout.write("No follow-ups for today.")
            return

        for lead in leads:
            if lead.assigned_to and lead.assigned_to.email:
                send_mail(
                    subject="Follow-Up Reminder",
                    message=f"""
Hello {lead.assigned_to.username},

You have a follow-up scheduled today.

Lead Name: {lead.name}
Phone: {lead.phone}
Email: {lead.email}
Remarks: {lead.remarks}

Please contact the client today.
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[lead.assigned_to.email],
                    fail_silently=False,
                )

        self.stdout.write(self.style.SUCCESS("Follow-up reminders sent successfully!"))