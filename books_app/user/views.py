from django.contrib.auth import login, logout
from rest_framework import views, generics, response, permissions, \
    authentication

from .serializers import UserSerializer, LoginSerializer


class RegisterUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class LoginView(views.APIView):
    """Create a new session for an user"""
    authentication_classes = (authentication.SessionAuthentication,)
    serializer_class = LoginSerializer

    def post(self, request):
        """Perform user login
        parameters: email, password
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data)


class LogoutView(views.APIView):
    """Logout APIView"""

    def post(self, request):
        """Perform user logout"""
        logout(request)
        return response.Response()


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
