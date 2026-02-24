# leads/models.py
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('pending', 'Pending'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    # Marketing Info
    source = models.CharField(max_length=100, blank=True, null=True)
    medium = models.CharField(max_length=100, blank=True, null=True)
    campaign = models.CharField(max_length=100, blank=True, null=True)
    
    INSTALLATION_TYPE_CHOICES = [
    ('residential', 'Residential'),
    ('commercial', 'Commercial'),
    ('industrial', 'Industrial'),
    ('offgrid', 'Off Grid'),
]

    installation_type = models.CharField(
    max_length=100,
    choices=INSTALLATION_TYPE_CHOICES,
    blank=True,
    null=True
)

    # Solar Details
    remarks = models.TextField(blank=True, null=True)
    roof_type = models.CharField(max_length=100, blank=True, null=True)
    average_monthly_bill = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    financing_preference = models.CharField(max_length=100, blank=True, null=True)
    sanctioned_load = models.CharField(max_length=100, blank=True, null=True)

    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Follow-up
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_time = models.TimeField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    def __str__(self):
        return self.name

    # Optional: Convenience property to check if follow-up is today
    @property
    def is_followup_today(self):
        from datetime import date
        return self.follow_up_date == date.today() if self.follow_up_date else False

    # Optional: Convenience property for overdue follow-ups
    @property
    def is_overdue(self):
        from datetime import date
        if self.follow_up_date:
          return self.follow_up_date < date.today()
        return False