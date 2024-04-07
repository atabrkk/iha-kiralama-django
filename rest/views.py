from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from ihas.models import Uav, Rental
from rest.serializers import UavSerializers, RentalSerializers, UserSerializer


class UavViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Uav.objects.all()
    serializer_class = UavSerializers


class RentalViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RentalSerializers

    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(user=user)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]