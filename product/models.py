from django.db import models


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
    first_category = models.CharField(max_length=128)
    second_category = models.CharField(max_length=128)

    def __str__(self):
        return self.product_name

    def find_substitute(self):
        results = Product.objects.filter(
            first_category=self.first_category,
            nutriscore_grade__lt=self.nutriscore_grade,
        ).order_by("nutriscore_grade", "nova_group")
        if not results:
            results = Product.objects.filter(
                first_category=self.second_category,
                nutriscore_grade__lt=self.nutriscore_grade,
            ).order_by("nutriscore_grade", "nova_group")
        return results
