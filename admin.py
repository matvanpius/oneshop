from django.contrib import admin
from .models import Customer, Mixed,Product,Order,OrderItem,ShippingAddress,All,Mixed,Vegetable,Spice,Snack,Oil,Legumes,Fruit

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class AllAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class MixedAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class VegetableAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class OilAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class FruitAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class SnackAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class SpiceAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')

class LegumesAdmin(admin.ModelAdmin):
    list_display = ('name','price','digital','image')       

admin.site.register( Customer)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register( OrderItem)
admin.site.register( ShippingAddress)
admin.site.register( All,AllAdmin)
admin.site.register( Mixed,MixedAdmin)
admin.site.register( Spice,SpiceAdmin)
admin.site.register( Oil,OilAdmin)
admin.site.register( Snack,SnackAdmin)
admin.site.register( Legumes,LegumesAdmin)
admin.site.register( Fruit,FruitAdmin)
admin.site.register( Vegetable,VegetableAdmin)

