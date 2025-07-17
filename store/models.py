from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"
    
    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity

