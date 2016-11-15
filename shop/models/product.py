from django.db import models

# Create your models here.
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class ProductQuerySet(models.query.QuerySet):
    """ класс-фильтр queryset - возвращает только продукты со статусом Active """

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    """ кастомный менеджер товаров"""

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()


class Product(models.Model):
    """ реализует класс Товар """
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    cross_sku = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)

    # slug
    objects = ProductManager()

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return "%s %s" % (self.manufacturer, self.sku)

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={'pk': self.id})
        # return "/shop/products/" + str(self.id)

    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&delete=true" % (reverse("cart"), self.id)


def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    return "products/%s_%s" % (instance.id, filename)


class ProductImage(models.Model):
    """ фоточки для товаров """
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to, null=True, blank=True)

    def __str__(self):
        return self.product.title
