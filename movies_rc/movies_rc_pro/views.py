from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import RegistrationSerializer,LoginSerializer,MovieSerializer
from collections import defaultdict


@api_view(['POST'])
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "User_created_successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # Check if the user exists and the password is correct
            user = User.objects.filter(email=email).first()
            if user and check_password(password, user.password):
                login(request, user)
                return Response({"status": "user_validated"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'status': 'Invalid_Credentials'}, status=status.HTTP_400_BAD_REQUEST)


from collections import defaultdict



@api_view(['GET'])
def movies_view(request):
    if request.user.is_authenticated:
        # Retrieve all movies
        movies_list = Movies.objects.all()

        # Group movies by their type directly
        movies_by_type = defaultdict(list)
        for movie in movies_list:
            # Group movies by their original type
            movies_by_type[movie.type].append(MovieSerializer(movie).data)

        # Convert defaultdict to a regular dictionary for the response
        response_data = {
            "movies": dict(movies_by_type)  # Wrap the result in the "movies" key
        }

        return Response(response_data)
    else:
        return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
        logout(request)
        return Response({"message": "Successfully_logged_out."}, status=status.HTTP_200_OK)
