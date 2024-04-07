from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest.views import UavViewSet, RentalViewSet, UserCreateAPIView

router = DefaultRouter()

router.register('uavs', UavViewSet)
router.register('user-reservations', RentalViewSet, basename="Rental")

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

]
