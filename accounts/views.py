from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializers import CustomUserSerializer


@api_view(['POST'])
def signup(request):
    """
    View to sign up new users in the platform.
    """

    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """
    API endpoint to log in a user.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request._request, email=email.lower(), password=password)

    if user is not None:
        login(request._request, user)
        return Response({'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)