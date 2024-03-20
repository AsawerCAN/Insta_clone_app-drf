from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.serializers import Serializer

from insta_app.models import User
from insta_app.serializers import UserLoginSerializer, UserSerializer


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginUserView(ObtainAuthToken):
    """
    Login user and return authentication token.
    """
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super(LoginUserView, self).post(request, *args, **kwargs)
        token = response.data.get('token')
        if token:
            response.data = {'success': True, 'token': token}
        return response


class RetrieveUser(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class UpdateUser(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "user updated"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyUser(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk):
        try:
            user = self.get_object()
            if user.id == request.user.id:
                self.perform_destroy(user)
                return Response({
                    "success": True,
                    "message": "user deleted"
                })
            else:
                return Response({
                    "success": False,
                    "message": "not enough permissions"
                }, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({
                "success": False,
                "message": "user does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
