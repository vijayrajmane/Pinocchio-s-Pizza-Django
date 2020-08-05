from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class pizza_category(models.Model):
    Name = models.CharField(max_length=100)
    def __str__(self):
          return f"{self.Name}"

class pizza(models.Model):
    category = models.ForeignKey(pizza_category, on_delete=models.CASCADE, default=1)
    Name = models.CharField(max_length=100)
    small_price = models.DecimalField(max_digits=4,decimal_places=2)
    large_price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
          return f"{self.category}  {self.Name}"

class topping(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Name}"

class sub(models.Model):
    Name = models.CharField(max_length=100)
    small_price = models.DecimalField(max_digits=4,decimal_places=2)
    large_price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.Name}"

class salad(models.Model):
    Name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.Name}"

class pasta(models.Model):
    Name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.Name}"

class dinner_platter(models.Model):
    Name = models.CharField(max_length=100)
    small_price = models.DecimalField(max_digits=4,decimal_places=2)
    large_price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
          return f"{self.Name}"

class user_order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_number = models.IntegerField()
    status = models.CharField(max_length =100, default='initiated')
    topping_allowance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.order_number} - {self.status}  Topping cnt:{self.topping_allowance}"

class order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    number=models.IntegerField()
    category=models.CharField(max_length=64,null=True)
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price} "

class Order_counter(models.Model):
    counter=models.IntegerField()

    def __str__(self):
        return f"Order no: {self.counter}  "
