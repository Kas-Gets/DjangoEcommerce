from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Product , Customer , Order , OrderItem, Address,UserToken
from .serializers import ProductSerializer , CustomerSerializer , OrderItemSerializer ,OrderSerializer,LoginSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate ,get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated  # Import permissions
from django.contrib.auth.models import User


##################### HANDLING USERS #############
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to access this view
def signup(request):
    """
    API view for customer signup
    """
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        # Create or get the token for the user using UserToken
        token, created = UserToken.objects.get_or_create(user=customer)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    API view for customer login
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Find user by email
        try:
            user = User.objects.get(email=email)  # Use your custom user model if applicable
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Compare the provided password with the stored password
        if user.password == password:
            token, created = UserToken.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# #####################  PRODUCTS #############
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def get_products(request):
    """
    API view to return a list of all products
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def get_product_detail(request, pk):
    """
    API view to return details of a single product by id (pk)
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def create_product(request):
    """
    API view to create a new product
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



# #####################  CUSTOMERS #############
@api_view(['GET'])
def get_customers(request):
    """
    API view to return a list of all customers
    """
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_customer_detail(request, pk):
    """
    API view to return details of a single customer by id (pk)
    """
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=404)
    
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

@api_view(['POST'])
def create_customer(request):
    """
    API view to create a new customer
    """
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)    




# ##################### ORDER #############

# Get all orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# Get order by ID
@api_view(['GET'])
def get_order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)

# Create a new order
@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Create a new order item
@api_view(['POST'])
def create_order_item(request):
    serializer = OrderItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Update the order's payment status
@api_view(['PATCH'])
def update_order_payment_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

    data = {'payment_status': request.data.get('payment_status')}
    serializer = OrderSerializer(order, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)