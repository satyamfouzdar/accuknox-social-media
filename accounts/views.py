from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.serializers import CustomUserSerializer
from accounts.models import CustomUser


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    """
    View to search for users using the query parameters of the get request.
    """
    query = request.GET.get('q', '')

    if query:
        users = CustomUser.objects.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).order_by('id')

        paginator = Paginator(users, 10)
        page = request.GET.get('page', 1)

        try:
            users_paginated = paginator.page(page)
        except EmptyPage:
            return JsonResponse({'error': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)

        users_list = [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users_paginated
        ]

        return JsonResponse({'users': users_list, 'total_pages': paginator.num_pages})

    return JsonResponse({'error': 'Please provide a valid search query'}, status=status.HTTP_400_BAD_REQUEST)