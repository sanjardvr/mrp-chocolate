from django.contrib import admin

from .models import BoM, BoMLine, ManufacturingOrder, Product

# Register your models here.

class BoMLineTab(admin.TabularInline):
    model = BoMLine
    extra = 2

@admin.register(BoM)
class BiMAdmin(admin.ModelAdmin):
    inlines = [BoMLineTab]

admin.site.register(Product)
admin.site.register(ManufacturingOrder)