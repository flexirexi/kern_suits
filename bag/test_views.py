from django.test import TestCase
from django.urls import reverse

class TestBagViews(TestCase):
    def test_add_to_bag_adds_correct_quantity(self):
        """Adds item to session bag and checks quantity"""
        self.client.post(reverse("add_to_bag"), {
            "variant_id": "123",
            "quantity": 2,
            "redirect_url": "/bag/"
        })
        bag = self.client.session["bag"]
        self.assertIn("123", bag)
        self.assertEqual(bag["123"], 2)

    def test_update_bag_changes_quantity(self):
        """Updates existing item quantity in session bag"""
        session = self.client.session
        session["bag"] = {"123": 1}
        session.save()

        self.client.post(reverse("update_bag", args=["123"]), {
            "quantity": 5,
            "redirect_url": "/bag/"
        })

        bag = self.client.session["bag"]
        self.assertEqual(bag["123"], 5)
        
    def test_remove_from_bag_deletes_item(self):
        """Removes item from session bag"""
        session = self.client.session
        session["bag"] = {"123": 1}
        session.save()

        self.client.post(reverse("remove_from_bag", args=["123"]), {
            "redirect_url": "/bag/"
        })

        bag = self.client.session["bag"]
        self.assertNotIn("123", bag)