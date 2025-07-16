from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Appointment(models.Model):
    APPOINTMENT_TYPES = [
        ("consultation", "Consultation"),
        ("fitting", "Fitting"),
        ("accessories", "Accessories advice"),
        ("pickup", "Pickup and check"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    appointment_type = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPES,
        default="consultation"
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.get_appointment_type_display()} am {self.start_datetime.strftime('%d.%m.%Y %H:%M')}"