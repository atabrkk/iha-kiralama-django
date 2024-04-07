from ihas.models import Uav, Rental
from rest_framework import serializers
from django.contrib.auth.models import User




class UavSerializers(serializers.ModelSerializer):
    class Meta:
        model = Uav
        fields = '__all__'

class RentalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id', 'username', 'password', 'password2', 'email', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
