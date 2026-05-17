from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import StudentRecord

class StudentRecordSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(
        source='owner.username', read_only=True
    )
    class Meta:
        model   = StudentRecord
        fields  = ['id','owner','owner_username','full_name',
                   'course','year_level','gpa','enrolled',
                   'created_at','updated_at']
        read_only_fields = ['id','owner','owner_username',
                            'created_at','updated_at']

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    email    = serializers.EmailField(required=False, allow_blank=True)
    role     = serializers.ChoiceField(choices=['Admin','Faculty','Student'])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        email = validated_data.pop('email', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=email,
        )
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        return user