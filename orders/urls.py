from django.urls import path

from . import views

urlpatterns = [

    path("login", views.login_view, name="login"),
    path("signin", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("menu/<str:category>", views.menu, name="menu"),
    path("add/<str:category>/<str:name>/<str:price>", views.add, name="add"),
    path("delete/<str:category>/<str:name>/<str:price>", views.delete, name="delete"),
    path("myorder/<int:order_number>", views.myOrder, name="myOrder"),
    path("confirm/<int:order_number>", views.confirm, name="confirm"),
    path("manageorder/<str:user>/<int:order_number>", views.manageOrder, name="manageOrder"),
    path("complete/<str:user>/<int:order_number>", views.completeOrder, name="completeOrder"),

    path("", views.index, name="index"),
]
