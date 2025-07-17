from products.fixtures.fixture_list_for_tests import BaseFixtureTestCase
from django.test import RequestFactory
from products.models import ProductVariant
from bag.contexts import bag_contents


class TestBagContextProcessor(BaseFixtureTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_total_from_existing_variant(self):
        variant = ProductVariant.objects.first()
    
        self.assertIsNotNone(variant, "No variant in DB.. test setup required")

        request = self.factory.get("/")
        request.session = {"bag": {str(variant.id): 2}}

        context = bag_contents(request)
        expected_total = variant.price * 2

        self.assertEqual(context["grand_total"], expected_total)
