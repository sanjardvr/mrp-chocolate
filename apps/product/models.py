from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    count = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name
    
class BoM(models.Model):
    ready_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='boms')

    class Meta:
        verbose_name = "Bill of Materials"
        verbose_name_plural = "Bills of Materials"

    def __str__(self):
        return f"Bom for {self.ready_product.name}"
    
class BoMLine(models.Model):
    ingridient = models.ForeignKey(Product, on_delete=models.CASCADE)
    bom = models.ForeignKey(BoM, on_delete=models.CASCADE, related_name='lines')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

class ManufacturingOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    producing_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    