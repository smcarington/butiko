from django.contrib import admin

from .models import ItemList, Item, PermRequest

admin.site.register(ItemList)
admin.site.register(Item)
admin.site.register(PermRequest)

# Register your models here.
