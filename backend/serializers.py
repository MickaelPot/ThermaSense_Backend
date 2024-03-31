from rest_framework import serializers
from .model_user import User
from .model_releve import Releve

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ReleveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Releve
        fields = '__all__'