import datetime
from decimal import Decimal

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    discount = models.IntegerField(default=0)  # type: ignore
    image = models.ImageField(upload_to="products/", default="default.jpg")
    description = models.TextField(blank=True, null=True)

    @property
    def discounted_price(self):
        return self.price * Decimal(str((1 - self.discount / 100))) #type: ignore

    @property
    def savings(self):
        print(self.price)
        print(self.discounted_price)
        print(self.price - self.discounted_price)

        return self.price - self.discounted_price

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # type: ignore
    address = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=10, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)  # type: ignore

    def __str__(self):
        return self.customer.name
