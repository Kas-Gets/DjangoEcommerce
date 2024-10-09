import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse


def product_list(request):
    return render(request, 'product_list.html')


def home(request):
    try:
        # Fetch all products from the API
        response = requests.get('http://localhost:8000/v1/api/products/')
        response.raise_for_status()
        products = response.json()

        # Get first 3 products for featured products
        # Adjust this line based on your logic to determine featured products
        featured_products = products[:3]
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        products = []
        featured_products = []

    return render(request, 'home.html', {'products': products, 'featured_products': featured_products})


def get_products(request):
    try:
        response = requests.get('http://localhost:8000/v1/api/products/')
        response.raise_for_status()
        products = response.json()
        return JsonResponse(products, safe=False)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def home(request):
    try:
        response = requests.get('http://localhost:8000/v1/api/products/')
        response.raise_for_status()
        # Get first 3 products for the home page
        products = response.json()[:3]
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        products = []

    return render(request, 'home.html', {'products': products})


def product_detail(request, id):
    try:
        response = requests.get(
            f'http://localhost:8000/v1/api/products/{id}/')
        response.raise_for_status()
        product = response.json()
    except requests.RequestException as e:
        print(f"Error fetching product details: {e}")
        product = None

    return render(request, 'product_detail.html', {'product': product})


def cart(request):
    return render(request, 'cart.html')


def checkout(request):
    return render(request, 'checkout.html')
