from .models import Profile
from .serializers import UserSerializer,AuthTokenSerializer, ProfileSerializer

from rest_framework import generics, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(ObtainAuthToken):

    serializer_class = AuthTokenSerializer

    def post(self, request, *args,**kwargs):
        serializers = self.serializer_class(data=request.data,context={'request':request})
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'roles':[user.is_active, user.is_staff],
        })
        
# class ProfileViewset(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Profile.objects.filter(user_id=user.id)
        return queryset