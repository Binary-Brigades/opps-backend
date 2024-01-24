from django.shortcuts import render
from .serializers import UserDetailsSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User

@api_view(['GET'])
def get_user_details(request):
    userId = request.user.id
    user = User.objects.get(id=userId)
    serializer = UserDetailsSerializer(user)
    print()
    return Response({serializer.data})


    
