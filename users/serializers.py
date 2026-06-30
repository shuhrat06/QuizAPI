from rest_framework import serializers
from .models import Group, User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class GroupForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id', 'name'
        ]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'role'
        ]
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'role'
        ]
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

class UserSelfUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name'
        ]
        kwargs = {
            'id': {
                'read_only': True
            }
        }


#Serializers for Swagger

class GroupAddTeacherSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()

class GroupAddStudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
