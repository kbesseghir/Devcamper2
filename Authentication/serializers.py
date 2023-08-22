from rest_framework import serializers
from .models import *




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Make password write-only

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name', 'role', 'created_at')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords must match.")
        return data