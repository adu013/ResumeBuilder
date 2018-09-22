from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=256, blank=True, null=True)
    alt_phone = models.CharField(max_length=15, blank=True, null=True)
    alt_email = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=1000, blank=True, null=True)
    experience = models.FloatField(null=True, blank=True)
    current_ctc = models.FloatField(null=True, blank=True)
    expected_ctc = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class UserJobExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    contribution = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)

