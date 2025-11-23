from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    # Cart
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("cart/increase/<int:product_id>/", views.cart_increase, name="cart_increase"),
    path("cart/decrease/<int:product_id>/", views.cart_decrease, name="cart_decrease"),

    # Auth
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Checkout / Receipt
    path("checkout/", views.checkout_view, name="checkout"),
    path("receipt/<int:order_id>/", views.receipt_view, name="receipt"),
]
