from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from products.models import Size, Fit, Color, Occasion


# Create your models here.
class UserProfile(models.Model):
    """ A custom userprofile model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # if it doesn't exist -> create it
        UserProfile.objects.get_or_create(user=instance)

    instance.userprofile.save()


class StyleProfile(models.Model):
    """Stores the user's size and style preferences"""
    user_profile = models.OneToOneField(
        'user.UserProfile',
        on_delete=models.CASCADE,
        related_name='style_profile'
    )

    # Sizes (optional)
    jacket_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, related_name='jacket_size_profiles')
    shirt_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, related_name='shirt_size_profiles')
    trousers_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, related_name='trousers_size_profiles')
    waistcoat_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, related_name='waistcoat_size_profiles')
    belt_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, related_name='belt_size_profiles')

    # Preferred colors
    preferred_color_1 = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_color1_profiles')
    preferred_color_2 = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_color2_profiles')
    preferred_color_3 = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_color3_profiles')

    # Fit preference
    fit_preference = models.ForeignKey(Fit, on_delete=models.SET_NULL, null=True, blank=True)

    # Occasions
    occasion_1 = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True, blank=True, related_name='occasion1_profiles')
    occasion_2 = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True, blank=True, related_name='occasion2_profiles')
    occasion_3 = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True, blank=True, related_name='occasion3_profiles')

    def __str__(self):
        return f"Style Profile for {self.user_profile.user.get_username()}"
