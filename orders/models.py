from django.db import models

# Create your models here.
from django.db import models
from users.models import Users, Product

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES=(
        ('pending','Pending'),
        ('shipped','Shipped'),
        ('delivered','Delivered')
    )
    user=models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )
    total_price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order {self.id}-{self.user.username}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity=models.IntegerField()
    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"