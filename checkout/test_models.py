
from decimal import Decimal
from django.test import override_settings
from django_countries.fields import Country
from checkout.models import Order, OrderItem
from products.models import ProductVariant
from products.fixtures.fixture_list_for_tests import BaseFixtureTestCase


class TestOrderModel(BaseFixtureTestCase):
    def setUp(self):
        super().setUp()
        self.variant = ProductVariant.objects.first()
        self.order = Order.objects.create(
            first_name="Gaius Julius",
            last_name="Cicero",
            email="cicery@atlantis.com",
            phone="123456789",
            address_line1="123 Main St",
            postal_code="12345",
            city="Atlantis",
            country=Country(code="DE")
        )

    def test_update_total_adds_delivery(self):
        """actually a simple test that update_total correctly adds item total + delivery"""
        OrderItem.objects.create(
            order=self.order,
            variant=self.variant,
            quantity=2,
            price=self.variant.price,
        )
        self.order.delivery_costs = Decimal("9.99")
        self.order.update_total()
        
        expected_total = self.variant.price * 2
        expected_grand = expected_total + Decimal("9.99")
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, expected_total)
        self.assertEqual(self.order.grand_total, expected_grand)

    def test_save_calculates_grand_total(self):
        """Test that .save() also sets grand_total as total + delivery"""
        
        self.order.total_amount = Decimal("100.00")
        self.order.delivery_costs = Decimal("15.00")
        self.order.save()

        self.order.refresh_from_db()
        self.assertEqual(self.order.grand_total, Decimal("115.00"))
