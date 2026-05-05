from django.db import models
from django.db import models
from users.models import Users, Product
# from products.models import 


# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity=models.IntegerField(default=1)

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','product')
    def __str__(self):
        return f"{self.user.username}-{self.product.name}"