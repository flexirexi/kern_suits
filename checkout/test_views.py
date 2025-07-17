from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from checkout.models import Order, OrderItem
from products.models import ProductVariant
from bag.contexts import bag_contents
from products.fixtures.fixture_list_for_tests import BaseFixtureTestCase


class TestCheckoutPost(BaseFixtureTestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="checkouttester",
            password="testpass123"
        )
        self.client.force_login(self.user)
        self.variant = ProductVariant.objects.first()
        self.bag = {str(self.variant.id): 2}
        session = self.client.session
        session["bag"] = self.bag
        session.save()

    def test_order_items_saved(self):
        """Checks that valid POST creates an order with correct order items"""
        response = self.client.post(reverse("checkout"), {
            "first_name": "Max",
            "last_name": "Mustermann",
            "email": "max@test.de",
            "phone": "12345678",
            "address_line1": "Musterstraße 1",
            "postal_code": "12345",
            "city": "Teststadt",
            "country": "DE",
            "client_secret": "pi_test_123_secret_xyz"
        })

        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 1)

        item = order.items.first()
        self.assertEqual(item.variant, self.variant)
        self.assertEqual(item.quantity, 2)

    def test_order_total_matches_bag(self):
        """Checks that order total equals expected bag total"""
        total_from_context = bag_contents(self.client.request().wsgi_request)["grand_total"]
        
        self.client.post(reverse("checkout"), {
            "first_name": "Max",
            "last_name": "Mustermann",
            "email": "max@test.de",
            "phone": "12345678",
            "address_line1": "Musterstraße 1",
            "postal_code": "12345",
            "city": "Teststadt",
            "country": "DE",
            "client_secret": "pi_test_123_secret_xyz"
        })

        order = Order.objects.last()
        item_total = sum(i.price * i.quantity for i in order.items.all())
        self.assertEqual(item_total, total_from_context)
