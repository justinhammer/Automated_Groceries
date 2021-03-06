from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=20)
    upc = models.CharField(max_length=25, default='DEFAULT')

    def __str__(self):
        return self.name
