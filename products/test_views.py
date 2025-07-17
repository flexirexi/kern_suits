# tests/test_reviews_service.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, ProductVariant, Category, Occasion, Series
from reviews.models import Review
from products.services.reviews import attach_review_data
from products.fixtures.fixture_list_for_tests import BaseFixtureTestCase


class TestAttachReviewData(BaseFixtureTestCase):
    def setUp(self):
        super().setUp()

        # Produkte aus der Test-Fixture
        self.product_with_reviews = Product.objects.get(id=1)
        self.product_without_reviews = Product.objects.get(id=2)

        # Zwei Testnutzer für die Reviews
        User = get_user_model()
        self.user_1 = User.objects.create_user(username="user1", email="user1@example.com", password="testpass")
        self.user_2 = User.objects.create_user(username="user2", email="user2@example.com", password="testpass")

    def test_product_with_multiple_reviews(self):
        """
        a product has multiple ratings
        """
        Review.objects.create(product=self.product_with_reviews, user=self.user_1, rating=5)
        Review.objects.create(product=self.product_with_reviews, user=self.user_2, rating=3)

        result = attach_review_data([self.product_with_reviews])
        product = result[0]

        self.assertEqual(product.review_count, 2)
        self.assertAlmostEqual(product.avg_rating, 4.0)

    def test_product_with_no_reviews(self):
        """
        a product has no ratings: avg_rating = None, count = 0
        """
        result = attach_review_data([self.product_without_reviews])
        product = result[0]

        self.assertEqual(product.review_count, 0)
        self.assertIsNone(product.avg_rating)


class TestProductMinPriceCalculation(BaseFixtureTestCase):
    def setUp(self):
        super().setUp()
        self.products = [Product.objects.get(id=i) for i in range(1, 4)]

        # Set up variants with different prices
        ProductVariant.objects.filter(product=self.products[0]).update(price=150)
        ProductVariant.objects.filter(product=self.products[1]).update(price=220)
        ProductVariant.objects.filter(product=self.products[2]).update(price=90)

    def test_min_price_is_correctly_set(self):
        for p in self.products:
            variants = p.variants.all()
            p.min_price = min([v.price for v in variants], default=None)
            p.max_price = max([v.price for v in variants], default=None)

        self.assertEqual(self.products[0].min_price, 150)
        self.assertEqual(self.products[1].min_price, 220)
        self.assertEqual(self.products[2].min_price, 90)

    def test_price_with_mixed_variant_prices(self):
        # Manuell einzelne Preise setzen
        v1 = self.products[0].variants.first()
        v1.price = 100
        v1.save()

        v2 = self.products[0].variants.last()
        v2.price = 300
        v2.save()

        variants = self.products[0].variants.all()
        self.products[0].min_price = min([v.price for v in variants])
        self.products[0].max_price = max([v.price for v in variants])

        self.assertEqual(self.products[0].min_price, 100)
        self.assertEqual(self.products[0].max_price, 300)

    def test_product_with_no_variants(self):
        # Create a new product with no variants

        self.category = Category.objects.get(id=1)
        self.occasion = Occasion.objects.get(id=1)
        self.series = Series.objects.get(id=1)
        product = Product.objects.create(
            name="NoVariantProduct", 
            is_active=True, 
            category=self.category,
            series=self.series,
            occasion=self.occasion)
        product.min_price = min([v.price for v in product.variants.all()], default=None)
        product.max_price = max([v.price for v in product.variants.all()], default=None)

        self.assertIsNone(product.min_price)
        self.assertIsNone(product.max_price)