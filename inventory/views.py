from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Product, StockLog, Category, Supplier
from .forms import ProductForm
from rest_framework import viewsets
from .serializers import ProductSerializer, StockLogSerializer
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token

# Custom decorator to check if the user is admin
def admin_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            # Generate or retrieve the token (optional)
            Token.objects.get_or_create(user=user)
            
            # Redirect to the product list page after successful registration
            return redirect('product_list')  # Redirect to any view you prefer
        else:
            return render(request, 'register.html', {'form': form, 'errors': form.errors})
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# Product Management Views
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@admin_required
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@admin_required
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

@admin_required
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

# Stock Management Views
@login_required
def add_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        product.quantity += quantity
        product.save()
        StockLog.objects.create(product=product, quantity_changed=quantity, reason='Stock added')
        return redirect('product_list')
    return render(request, 'add_stock.html', {'product': product})

@login_required
def remove_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if product.quantity >= quantity:
            product.quantity -= quantity
            product.save()
            StockLog.objects.create(product=product, quantity_changed=-quantity, reason='Stock removed')
            return redirect('product_list')
        else:
            return render(request, 'remove_stock.html', {'product': product, 'error': 'Not enough stock'})
    return render(request, 'remove_stock.html', {'product': product})

# Reporting View
@login_required
def report(request):
    # Calculate total inventory value
    total_value = sum(product.quantity * product.price for product in Product.objects.all())

    # Filter and sort products based on request parameters
    products = Product.objects.all()

    # Filtering
    category_filter = request.GET.get('category')
    supplier_filter = request.GET.get('supplier')
    stock_filter = request.GET.get('stock_level')

    if category_filter:
        products = products.filter(category__name=category_filter)
    
    if supplier_filter:
        products = products.filter(supplier__name=supplier_filter)
    
    if stock_filter:
        if stock_filter == 'low':
            products = products.filter(quantity__lt=5)
        elif stock_filter == 'high':
            products = products.filter(quantity__gte=5)

    # Sorting
    sort_order = request.GET.get('sort_order', 'asc')  # Default to ascending
    if sort_order == 'desc':
        products = products.order_by('-quantity')
    else:
        products = products.order_by('quantity')

    categories = Category.objects.all()  # For filtering by category
    suppliers = Supplier.objects.all()  # For filtering by supplier

    return render(request, 'report.html', {
        'total_value': total_value,
        'products': products,
        'categories': categories,
        'suppliers': suppliers,
        'stock_filter': stock_filter,
        'sort_order': sort_order,
    })

# API Views
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all API requests

class StockLogViewSet(viewsets.ModelViewSet):
    queryset = StockLog.objects.all()
    serializer_class = StockLogSerializer
    permission_classes = [IsAuthenticated]