from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    product_image = models.ImageField(upload_to="product/Image", null=True)
    info = models.TextField()

    def __str__(self) -> str:
        return self.name
