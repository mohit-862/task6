from django.contrib import admin
from .models import Customuser,Product,Category

# Register your models here.
admin.site.register(Customuser)
admin.site.register(Product)
admin.site.register(Category)

