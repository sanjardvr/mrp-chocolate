from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Product
from .service import produce


def dashboard(request):
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        raw_quantity = request.POST.get("quantity", "")


        try:
            quantity = Decimal(raw_quantity)
        except InvalidOperation:
            messages.error(request, "Invalid quantity. Please enter a valid number.")
            return redirect('dashboard')

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect('dashboard')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('dashboard')

        try:
            produce(product, quantity)
            messages.success(request, f"Successfully produced {quantity} units of {product.name}.")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard')

    return render(request, 'products/dashboard.html', {'products': products})