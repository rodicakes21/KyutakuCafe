from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Order, CheckoutItem
from .cart import Cart  # Your custom Cart class

# Home page / product list
def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


# Product detail
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


# Cart views using custom Cart class
@login_required
def cart_view(request):
    cart = Cart(request)
    return render(request, "store/cart.html", {"cart": cart})


@login_required
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.add(product=product)
    return redirect("cart")


@login_required
def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    return redirect("cart")


@login_required
def cart_increase(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.add(product=product, quantity=1)
    return redirect("cart")


@login_required
def cart_decrease(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.add(product=product, quantity=-1)
    item = cart.cart.get(str(product_id))
    if item and item["quantity"] <= 0:
        cart.remove(product)
    return redirect("cart")


# User login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


# User registration
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully. You can login now.")
        return redirect('login')

    return render(request, 'store/register.html')


# User logout
def logout_view(request):
    logout(request)
    return redirect('home')


# Checkout view
@login_required
def checkout_view(request):
    cart = Cart(request)
    cart_items = list(cart)  # list of dicts from your Cart class
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Create Order
        order = Order.objects.create(
            user=request.user,
            customer_name=name,
            address=address,
            email=email,
            phone=phone
        )

        # Add each cart item to CheckoutItem
        for item in cart_items:
            CheckoutItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                total_price=item["total_price"]
            )

        # Clear the cart
        cart.clear()

        messages.success(request, "Order placed successfully!")
        return redirect('receipt', order_id=order.id)

    cart_total = sum(item["total_price"] for item in cart_items)
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'store/checkout.html', context)


# Receipt view
@login_required
def receipt_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/receipt.html', {'order': order})
