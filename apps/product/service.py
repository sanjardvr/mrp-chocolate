from django.core.exceptions import ValidationError
from django.db import transaction

from .models import ManufacturingOrder


@transaction.atomic
def produce(product, quantity):
    bom = product.boms.first()
    if not bom:
        raise ValidationError(
            f"No Bill of Materials found for {product.name}"
        )

    if quantity <= 0:
        raise ValidationError("Producing quantity must be greater than zero.")

    for line in bom.lines.select_related('ingridient').all():
        required = line.quantity * quantity
        if line.ingridient.count < required:
            raise ValidationError(
                f"Not enough {line.ingridient.name}. "
                f"Need {required}, but only have {line.ingridient.count}."
            )

    for line in bom.lines.select_related('ingridient').all():
        required = line.quantity * quantity
        line.ingridient.count -= required
        line.ingridient.save()

    product.count += quantity
    product.save()

    order = ManufacturingOrder.objects.create(
        product=product,
        producing_quantity=quantity,
    )

    return order