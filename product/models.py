from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image_url = models.URLField(max_length=255)
    nova_group = models.CharField(max_length=1)
    nutriscore_grade = models.CharField(max_length=1)
    saturated_fat_100g = models.DecimalField(
        max_digits=6, decimal_places=3, null=True
    )
    fat_100g = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    salt_100g = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    sugars_100g = models.DecimalField(
        max_digits=6, decimal_places=3, null=True
    )
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.product_name

    def find_substitute(self):
        res = list()
        product_categories = set(self.categories.all())
        for product in Product.objects.filter(
            nutriscore_grade__lt=self.nutriscore_grade
        ).order_by("nutriscore_grade"):
            if (
                len(
                    product_categories.intersection(
                        set(product.categories.all())
                    )
                )
                > 4
            ):
                res.append(product)
        return res
