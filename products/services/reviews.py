from django.db.models import Avg, Count
from reviews.models import Review


# outsource ratings logic as views.py becomes too large..
def attach_review_data(products):
    """
    Adds avg_rating and review_count attributes to each product of the product model
    """
    product_ids = [p.id for p in products]
    review_stats = (
        Review.objects
        .filter(product_id__in=product_ids)
        .values("product_id")
        .annotate(
            avg_rating=Avg("rating"),
            review_count=Count("id")
        )
    )
    data = {
        item["product_id"]: {
            "avg_rating": item["avg_rating"],
            "review_count": item["review_count"],
        }
        for item in review_stats
    }

    for product in products:
        stats = data.get(product.id)
        if stats:
            product.avg_rating = stats["avg_rating"]
            product.review_count = stats["review_count"]
        else:
            product.avg_rating = None
            product.review_count = 0

    return products
