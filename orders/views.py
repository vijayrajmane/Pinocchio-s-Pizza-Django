from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db.models import Sum

from .models import Category,pizza_category,pizza,salad,pasta,topping,dinner_platter,sub,user_order,order,Order_counter

# Create your views here.


counter = Order_counter.objects.first()
if counter==None:
    set_counter=Order_counter(counter=1)
    set_counter.save()

superuser = User.objects.filter(is_superuser=True)
if superuser.count() == 0:
    superuser=User.objects.create_user("admin","admin@admin.com","admin@1234")
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()
    set_superuser=User_order(user=superuser,order_number=counter.counter)
    set_superuser.save()


def index(request):
    if not request.user.is_authenticated:
        return render(request,"orders/login.html")

    order_number = user_order.objects.get(user=request.user,status='initiated').order_number
    context = {
        "user":request.user,
        "Checkout":order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        'Category': Category.objects.all(),
        "Order_number":order_number
    }
    return render(request,"orders/index.html",context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('/')
        
    return render(request, "orders/login.html",{'message_fail': "Invalid username or password"})

def logout_view(request):
    logout(request)
    return render(request,"orders/login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username =request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password !=password2:
            return render(request,"orders/register.html",{"message_fail":"Passwords don't match."})
        user=User.objects.create_user(username,email=email,password=password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        counter=Order_counter.objects.first()
        order_number=user_order(user=user,order_number=counter.counter)
        order_number.save()
        counter.counter=counter.counter+1
        counter.save()
        
        
        return render(request, "orders/login.html",{'message_success':"Registered!!.You can login now"})
    return render(request,"orders/register.html")

def menu(request,category):
    menu,columns=findTable(category)
    try:
        order_number = user_order.objects.get(user=request.user, status='initiated').order_number
    except user_order.DoesNotExist:
        pass
    
    context = {
        "user":request.user,
        "Checkout":order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        'Category': Category.objects.all(),
        'Menu':menu,
        'Columns':columns,
        'Current_category':category,
        "Topping_price": 0.00,
        "Order_number":order_number,
    }
    return render(request, "orders/menu.html",context)

def add(request,category,name, price):
    menu,columns=findTable(category)
    
    order_number = user_order.objects.get(user=request.user, status='initiated').order_number
    topping = user_order.objects.get(user=request.user,status='initiated')

    context = {
        'Checkout':order.objects.filter(user=request.user, number = order_number),
        "Checkout_category":order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        'Current_category':category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }

    if (category == 'Regular Pizza' or category == 'Sicilian Pizza'):
        if name =="1 topping" or name=='1 item':
            topping.topping_allowance+=1
            topping.save()
        if name =="2 toppings" or name=='2 item':
            topping.topping_allowance+=2
            topping.save()
        if name =="3 toppings" or name=='3 item':
            topping.topping_allowance+=3    
            topping.save()
    if category == "Toppings" and topping.topping_allowance == 0:
        return render(request,"orders/menu.html",context) 
    if category == "Toppings" and topping.topping_allowance > 0:
        topping.topping_allowance-=1
        topping.save()

    add = order(user = request.user, number = order_number, category = category, name = name, price = price )
    add.save()

    context2 = {
        'Checkout':order.objects.filter(user=request.user, number = order_number),
        "Checkout_category":order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        'Current_category': category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }

    return render(request,"orders/menu.html",context2)

def delete(request,category,name,price):
    menu,columns=findTable(category)
    
    order_number = user_order.objects.get(user=request.user, status='initiated').order_number
    topping = user_order.objects.get(user=request.user,status='initiated')
    
    if category == 'Regular Pizza' or category == 'Sicilian Pizza':
        if name == '1 topping' or name == '1 item':
            topping.topping_allowance -= 1
        if name == '2 topping' or name == '2 item':
            topping.topping_allowance -= 2
        if name == '3 topping' or name == '3 item':
            topping.topping_allowance -= 1
        topping.topping_allowance = 0
        topping.save()
        delete_topping = order.objects.filter(user = request.user, category = 'Toppings')
        delete_topping.delete()
        if category == 'Toppings':
            topping.topping_allowance += 1
            topping.save()

    delete_order = order.objects.filter(user = request.user, category = category, name = name, price = price)[0]
    delete_order.delete()

    context = {
        'Checkout':order.objects.filter(user=request.user, number = order_number),
        "Checkout_category":order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        'Current_category': category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }

    return render(request, "orders/menu.html", context)

def myOrder(request, order_number):
    context = {
        'user': request.user,
        "Checkout":order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "All_orders":user_order.objects.filter(user=request.user),
        "Status":user_order.objects.get(user=request.user,order_number=order_number).status,
        "Total":list(order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number":order_number,
    }
    return render(request, "orders/myOrder.html",context)

def confirm(request, order_number):
    order = user_order.objects.get(user=request.user,order_number=order_number)
    order.status = 'pending'
    order.save()

    counter=Order_counter.objects.first()
    new_order_number=user_order(user=request.user,order_number=counter.counter)
    new_order_number.save()
    counter.counter=counter.counter+1
    counter.save()
    return myOrder(request,order_number)

def manageOrder(request,user, order_number):
    user = User.objects.get(username = user)
    context = {
        "Checkout":order.objects.filter(user=user,number=order_number),
        "Checkout_category":order.objects.filter(user=user,number=order_number).values_list('category').distinct(),
        "Total":list(order.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Order_number":order_number,
        "All_orders":user_order.objects.exclude(status='initiated')
    }
    return render(request, "orders/manageOrder.html", context)

def completeOrder(request,user,order_number):
    user = User.objects.get(username = user)
    completeOrder = user_order.objects.get(user = user, order_number = order_number)
    completeOrder.status = 'completed'
    completeOrder.save()
    context = {
        "Checkout":order.objects.filter(user=user,number=order_number),
        "Checkout_category":order.objects.filter(user=user,number=order_number).values_list('category').distinct(),
        "Total":list(order.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Order_number":order_number,
        "All_orders":user_order.objects.exclude(status='initiated')
    }
    return render(request, "orders/manageOrder.html", context)

def findTable(category):
    if category == 'Regular Pizza':
        q = pizza_category.objects.filter(Name='Regular Pizza')
        for x in q:
            if x.Name=='Regular Pizza':
                menu = pizza.objects.filter(category=x.id)
        columns=3
    elif category == "Sicilian Pizza":
        q = pizza_category.objects.filter(Name='Sicilian Pizza')
        for x in q:
            if x.Name=='Sicilian Pizza':
                menu = pizza.objects.filter(category=x.id)
        columns=3
    elif category == "Toppings":
        menu=topping.objects.all()
        columns=1
    elif category == "Subs":
        menu=sub.objects.all()
        columns=3
    elif category == "Pasta":
        menu=pasta.objects.all()
        columns=2
    elif category == "Salads":
        menu=salad.objects.all()
        columns=2
    elif category == "Dinner Platters":
        menu=dinner_platter.objects.all()
        columns=3

    return menu,columns   
