import pytz
from rest_framework import serializers
from .models import User, Lead, Project


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'password', 'status', 'last_login', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_last_login(self, obj):
        if obj.last_login:
            timezone_br = pytz.timezone('America/Sao_Paulo')
            last_login_br = obj.last_login.astimezone(timezone_br)
            formatted_date = last_login_br.strftime("%d de %b de %Y %H:%M:%S")
            return formatted_date
        else:
            return None


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)  # Campo de leitura adicional para o nome do lead no serializer de Projects

    class Meta:
        model = Project
        fields = '__all__'


