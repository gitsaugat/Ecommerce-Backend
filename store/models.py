from io import BytesIO
from django.db import models
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import User
import math


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def get_products(self):
        return self.category_products.all()

    def get_absolute_url(self) -> str:
        return f'/{self.slug}/'


class Products(models.Model):

    category = models.ForeignKey(
        Category, related_name="category_products", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f'/{self.slug}/'

    def get_image_url(self) -> str:
        url = ''
        try:
            url = self.image.url
        except:
            url = ''

        return url

    def get_thumbnail_url(self) -> str:
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.create_thumbnail(self.image)
                return self.thumbnail.url

    def create_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


class Order(models.Model):
    user = models.ForeignKey(User, related_name="user_orders",
                             on_delete=models.DO_NOTHING)
    slug = models.SlugField(default="order", blank=False, null=False)
    transaction_id = models.CharField(
        max_length=250, default="transaction-id", blank=False, null=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'order-{self.slug}'

    def get_cart_total(self):
        data = [endpoint.get_total for endpoint in self.orderitem_orders.all()]
        return math.trunc(sum(data))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="orderitem_orders", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Products, related_name="products", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return str(self.order)

    @property
    def get_total(self):
        return self.product.price * self.quantity
