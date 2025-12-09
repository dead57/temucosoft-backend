from rest_framework import serializers
from .models import User, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # Mostramos el nombre de la empresa para facilitar el frontend
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rut', 'role', 'company', 'company_name', 'password')
        extra_kwargs = {'password': {'write_only': True}} # La contraseña nunca se devuelve al leer

    def create(self, validated_data):
        # Encriptamos la contraseña antes de guardar
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance