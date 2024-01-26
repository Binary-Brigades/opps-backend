from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet


from .models import User,Category
from .serializers import UserDetailsSerializer,CategorySerializer

@api_view(['GET'])
def get_user_details(request):
    print(request.user)
    try:
        userId = request.user.id
        user = User.objects.get(id=userId)
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error':'user does not exist'})

class CategoryViewSet(ModelViewSet):
    # model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    
    


    
