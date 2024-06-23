from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from ..models.userModel import User
from ..serializers.userSerializer import UserSerializer


class UserViews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


def create(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@action(detail=False, methods=["post"], permission_classes=[AllowAny])
def login(self, request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"})
    else:
        return Response(
            {"message": "Invalide credientials"}, status=status.HTTP_400_BAD_REQUEST
        )


@action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
def logout(self, request):
    logout(request)
    return Response({"message": "User logged out"}, status=status.HTTP_200_OK)
