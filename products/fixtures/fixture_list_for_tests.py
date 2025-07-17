from django.test import TestCase

class BaseFixtureTestCase(TestCase):
    """
    all test from all apps need to create test DBs 
    otherwise tests rarely make sense and django 
    cant test real DBs, so, we fill the test DBs (again)
    """
    fixtures = [
        "products/fixtures/category_fixture.json",
        "products/fixtures/occasion_fixture.json",
        "products/fixtures/series_fixture.json",
        "products/fixtures/products_fixture.json",
        "products/fixtures/fit_fixture.json",
        "products/fixtures/size_fixture.json",
        "products/fixtures/color_fixture.json",
        "products/fixtures/variants_fixture.json",
    ]