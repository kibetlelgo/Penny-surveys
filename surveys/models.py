from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    referral_code = models.CharField(max_length=50, blank=True, null=True)
    mpesa_number = models.CharField(max_length=20, blank=True, null=True)
    has_taken_first_survey = models.BooleanField(default=False)
    has_active_subscription = models.BooleanField(default=False)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    surveys_completed = models.IntegerField(default=0)
    system_survey_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
