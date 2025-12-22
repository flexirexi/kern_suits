from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from decimal import Decimal
from products.models import (
    ProductVariant,
    Product,
    Series,
    Category,
    Occasion,
    Fit,
    Size,
    Color
)

NEW_SENTINEL = "NEW"


class ProductVariantForm(forms.ModelForm):
    """
    A single form that creates a new product variant. Since a variant is
    always bound to a product, the user should be able to create a
    product or a series, too. This class will also handle that.
    """

# --- Choice fields with a "NEW" option ---
    series_choice = forms.ChoiceField(
        label="Select series",
        required=True,
        help_text="Pick an existing series or choose “➕ New series …”."
    )
    product_choice = forms.ChoiceField(
        label="Select product",
        required=True,
        help_text="Pick an existing product or choose “➕ New product …”."
    )

    # --- New Series fields (only used when series_choice == NEW) ---
    new_series_name = forms.CharField(label="New series: name", required=False)
    new_series_slug = forms.SlugField(
        label="New series: slug (optional)", required=False)
    new_series_description = forms.CharField(
        label="New series: description",
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False
    )
    new_series_is_active = forms.BooleanField(
        label="New series is active",
        required=False,
        initial=True
    )

    # --- New Product fields (only used when product_choice == NEW) ---
    new_product_name = forms.CharField(
        label="New product: name", required=False)
    new_product_slug = forms.SlugField(
        label="New product: slug (optional)", required=False)
    new_product_description = forms.CharField(
        label="New product: description",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False
    )
    new_product_fabric = forms.CharField(
        label="New product: fabric", required=False)
    new_product_is_active = forms.BooleanField(
        label="New product is active",
        required=False,
        initial=True
    )
    new_product_category = forms.ModelChoiceField(
        label="New product: category",
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    new_product_occasion = forms.ModelChoiceField(
        label="New product: occasion",
        queryset=Occasion.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    new_product_image = forms.ImageField(
        label="New product: image (optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    # --- Variant fields (from model) ---
    fit = forms.ModelChoiceField(
        label="Fit",
        queryset=Fit.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    size = forms.ModelChoiceField(
        label="Size",
        queryset=Size.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    color = forms.ModelChoiceField(
        label="Color",
        queryset=Color.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    price = forms.DecimalField(
        label="Price (€)",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": "0.01", "min": "0"})
    )
    stock = forms.IntegerField(
        label="Stock (qty)",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    sku = forms.CharField(
        label="SKU",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        label="Variant is active",
        required=False,
        initial=True
    )

    class Meta:
        model = ProductVariant
        fields = ["fit", "size", "color", "price", "stock", "sku", "is_active"]

    def __init__(self, *args, **kwargs):
        """
        Populate the dropdowns and set common widget classes.
        """
        super().__init__(*args, **kwargs)

        # Series choices: empty → NEW → existing
        series_choices = [("", "— Select —"), (NEW_SENTINEL, "➕ New series …")]
        series_choices += [
            (str(s.id), s.name) for s in Series.objects.order_by("name")
        ]
        self.fields["series_choice"].choices = series_choices
        self.fields["series_choice"].widget.attrs.update(
            {"class": "form-select"})

        # Product choices: empty → NEW → existing
        product_choices = [
            ("", "— Select —"), (NEW_SENTINEL, "+ New product …")
        ]
        product_choices += [
            (str(p.id), p.name) for p in Product.objects.order_by("name")
        ]
        self.fields["product_choice"].choices = product_choices
        self.fields["product_choice"].widget.attrs.update(
            {"class": "form-select"})

        # Ensure consistent styling on text inputs/areas
        for f in ["new_series_name", "new_series_slug"]:
            self.fields[f].widget.attrs.update({"class": "form-control"})
        self.fields["new_series_description"].widget.attrs.update(
            {"class": "form-control"})

        for f in [
            "new_product_name",
            "new_product_slug",
            "new_product_fabric"
        ]:
            self.fields[f].widget.attrs.update({"class": "form-control"})
        self.fields["new_product_description"].widget.attrs.update(
            {"class": "form-control"})

        # UI-Hints (nicht ausreichend alleine, aber hilfreich)
        if "price" in self.fields:
            self.fields["price"].widget.attrs.update(
                {"min": "0", "step": "0.01"}
            )
        if "stock" in self.fields:
            self.fields["stock"].widget.attrs.update({"min": "0", "step": "1"})

    def clean_price(self):
        val = self.cleaned_data.get("price")
        if val is not None and val < Decimal("0"):
            raise ValidationError("Price cannot be negative.")
        return val

    def clean_stock(self):
        val = self.cleaned_data.get("stock")
        if val is not None and val < 0:
            raise ValidationError("Stock cannot be negative.")
        return val

    # --------------------- Validation ---------------------
    def clean(self):
        """
        Validate the intent (existing vs NEW), auto-generate slugs when
        omitted, ensure required fields for NEW branches, and pre-check
        SKU uniqueness.
        """
        cleaned = super().clean()
        series_choice = cleaned.get("series_choice")
        product_choice = cleaned.get("product_choice")

        # NEW Series branch: require name; auto-slug if omitted
        if series_choice == NEW_SENTINEL:
            if not cleaned.get("new_series_name"):
                self.add_error(
                    "new_series_name",
                    "Please provide a series name."
                )
            if not cleaned.get("new_series_slug") and cleaned.get(
                "new_series_name"
            ):
                cleaned["new_series_slug"] = slugify(
                    cleaned["new_series_name"])

        # NEW Product branch: require core fields; auto-slug if omitted
        if product_choice == NEW_SENTINEL:
            required_new_product_fields = [
                "new_product_name", "new_product_category",
                "new_product_occasion", "new_product_fabric"
            ]
            for f in required_new_product_fields:
                if not cleaned.get(f):
                    self.add_error(f, "This field is required.")
            if not cleaned.get("new_product_slug") and cleaned.get(
                "new_product_name"
            ):
                cleaned["new_product_slug"] = slugify(
                    cleaned["new_product_name"])

        # If both IDs chosen (existing series & product): ensure product
        # belongs to series
        if series_choice not in (
            "",
            NEW_SENTINEL
        ) and product_choice not in (
            "",
            NEW_SENTINEL
        ):
            try:
                s = Series.objects.get(id=int(series_choice))
                p = Product.objects.get(id=int(product_choice))
                if p.series_id != s.id:
                    self.add_error(
                        "product_choice",
                        "The product doesn't belong to the selected series."
                    )
            except (Series.DoesNotExist, Product.DoesNotExist, ValueError):
                # Let default errors surface elsewhere if needed
                pass

        # Early checks for SKU uniqueness
        sku = cleaned.get("sku")
        if sku and ProductVariant.objects.filter(sku=sku).exists():
            self.add_error("sku", "This SKU already exists.")

        # Variant duplication check will run in save(), once the final
        # Product is known.
        return cleaned

    # ----------------------- Save ------------------------

    def save(self, commit=True):
        """
        Resolve or create Series/Product based on choices,
        then create the ProductVariant. If product is NEW and an
        image is provided, store it in Product.image.
        """
        cleaned = self.cleaned_data

        # 1) Resolve or create Series
        series_choice = cleaned["series_choice"]
        if series_choice == NEW_SENTINEL:
            series = Series.objects.create(
                name=cleaned["new_series_name"],
                slug=cleaned["new_series_slug"] or slugify(
                    cleaned["new_series_name"]),
                description=cleaned.get("new_series_description", ""),
                is_active=cleaned.get("new_series_is_active", True),
            )
        else:
            series = Series.objects.get(id=int(series_choice))

        # 2) Resolve or create Product
        product_choice = cleaned["product_choice"]
        if product_choice == NEW_SENTINEL:
            product = Product(
                category=cleaned["new_product_category"],
                occasion=cleaned["new_product_occasion"],
                series=series,
                name=cleaned["new_product_name"],
                slug=cleaned["new_product_slug"] or slugify(
                    cleaned["new_product_name"]),
                description=cleaned.get("new_product_description", ""),
                fabric=cleaned["new_product_fabric"],
                is_active=cleaned.get("new_product_is_active", True),
            )
            img = cleaned.get("new_product_image")
            if img:
                product.image = img
            if commit:
                product.save()
        else:
            product = Product.objects.get(id=int(product_choice))

        # 3) Create the variant for the resolved product
        instance = ProductVariant(
            product=product,
            fit=cleaned["fit"],
            size=cleaned["size"],
            color=cleaned["color"],
            price=cleaned.get("price"),
            stock=cleaned.get("stock") or 0,
            sku=cleaned["sku"],
            is_active=cleaned.get("is_active", True),
        )

        # Final check for (product, fit, size, color)
        if ProductVariant.objects.filter(
            product=product,
            fit=instance.fit,
            size=instance.size,
            color=instance.color
        ).exists():
            raise ValidationError(
                "The variant combination already exists for "
                "the selected product.")

        if commit:
            instance.save()
        return instance
