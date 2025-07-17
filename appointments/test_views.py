from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from appointments.models import Appointment

class TestAppointmentsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", password="pass")
        self.client.login(username="test", password="pass")
        self.url = reverse("appointments")
        self.future_dt = (datetime.now() + timedelta(days=1)).replace(hour=14, minute=0, second=0, microsecond=0)

    def test_get_view_loads_with_context(self):
        """Basic GET loads page with booked_slots and form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("booked_slots", response.context)
        self.assertIn("form", response.context)


    def test_existing_appointment_appears_in_booked_slots(self):
        """Saved appointment shows up correctly in booked_slots"""
        Appointment.objects.create(user=self.user, start_datetime=self.future_dt)
        response = self.client.get(self.url)
        key = self.future_dt.date().isoformat()
        self.assertIn(key, response.context["booked_slots"])
        self.assertIn(14, response.context["booked_slots"][key])
