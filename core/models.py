from django.conf import settings
from django.db import models
from django.db.models.functions import Round
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('H', 'Hoodies'),
)

LABEL_CHOICES = (
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger'),
)


# Items shown in products page
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    image = models.ImageField(upload_to="img/%y")
    slug = models.SlugField(default="test-product")
    description = models.TextField()
    additional_image1 = models.ImageField(
        upload_to="img/%y", blank=True, null=True)
    additional_image2 = models.ImageField(
        upload_to="img/%y", blank=True, null=True)
    additional_image3 = models.ImageField(
        upload_to="img/%y", blank=True, null=True)
    additional_info = models.TextField(default="This is a description field.")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:cart_add", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:cart_remove", kwargs={
            'slug': self.slug
        })


# Items of the Order List
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amt_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()


# Order List shown in Cart
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    items = models.ManyToManyField(OrderItem)
    # Moment the order was created
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_coupon(self):
        total = 0
        total = self.get_total() - Coupon.discount
        return total
