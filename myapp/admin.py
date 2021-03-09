from django.contrib import admin
from myapp.models import Contact,Category,Register,add_product,cart,Order
# Register your models here.

class add_productAdmin(admin.ModelAdmin):
    list_display = ["id","seller_name","product_name","product_category","product_price","sale_price"]

class RegisterAdmin(admin.ModelAdmin):
    list_display=["id","user","profile_pic","contact_number","gender","address"]

admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(cart)
admin.site.register(Register,RegisterAdmin)
admin.site.register(add_product,add_productAdmin)
admin.site.register(Order)
