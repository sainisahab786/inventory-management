from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    # Threshold for low stock alert
    LOW_STOCK_THRESHOLD = 5

    def is_low_stock(self):
        return self.quantity < self.LOW_STOCK_THRESHOLD

    def __str__(self):
        return self.name

class StockLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    date_changed = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_changed} - {self.date_changed}"
