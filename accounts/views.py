from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not name or not email or not password:
        return Response({
            "error": "name, email, password required"
        }, status=400)

    if User.objects.filter(email=email).exists():
        return Response({
            "error": "Email already exists"
        }, status=400)

    user = User.objects.create_user(
        name=name,
        email=email,
        password=password
    )
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "User created successfully",
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh)
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(
        username=email,
        password=password
    )
    if user is None:
        return Response({
            "error": "Invalid credentials"
        }, status=401)
    refresh = RefreshToken.for_user(user)
    return Response({
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh)
    })