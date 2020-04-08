from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Campaign(models.Model):
    title = models.TextField()
    description = models.TextField()
    auto_fb_post_mode = models.BooleanField()
    currencycode = models.TextField()
    goal = models.IntegerField()
    donators = models.IntegerField()
    days_active = models.IntegerField()
    has_beneficiary = models.BooleanField()
    status = models.BooleanField()
    deactivated = models.BooleanField()
    campaign_hearts = models.IntegerField()
    social_share_total = models.IntegerField()
    location_country = models.TextField()
    is_charity = models.BooleanField()
    charity_valid = models.BooleanField()
    avg_donation = models.DecimalField(max_digits=10, decimal_places=2)
    c_rating = models.IntegerField(null=True, blank=True)

