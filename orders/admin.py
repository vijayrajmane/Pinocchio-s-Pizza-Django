from django.contrib import admin
from .models import pizza_category,pizza,topping,sub,salad,pasta,dinner_platter,Category,user_order,Order_counter,order
# Register your models here.
admin.site.register(pizza)
admin.site.register(pizza_category)
admin.site.register(topping)
admin.site.register(sub)
admin.site.register(salad)
admin.site.register(pasta)
admin.site.register(dinner_platter)
admin.site.register(Category)
admin.site.register(user_order)
admin.site.register(order)
admin.site.register(Order_counter)