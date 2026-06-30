from rest_framework import serializers
from .models import (
    Quiz,
    Question,
    Option,
    Submission,
    StudentAnswer
)
from users.models import User, Group

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name'
        ]

class QuizCreateSerializer(serializers.ModelSerializer):
    allowed_students = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.filter(role='student'),
        many = True
    )
    class Meta:
        model = Quiz
        exclude = ['created_by']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Tugash vaqti boshlanish vaqtidan keyin bo'lishi kerak")
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        students = validated_data.pop('allowed_students')
        quiz = Quiz.objects.create(
            created_by = user,
            **validated_data
        )
        quiz.allowed_students.set(students)

        return quiz

class QuizDetailSerializer(serializers.ModelSerializer):
    created_by = UserShortSerializer(read_only=True)
    class Meta:
        model = Quiz
        exclude = ['allowed_students']

class QuizUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        exclude = ['created_by', 'allowed_students']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class QuestionReadSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'text', 'options']
    def get_options(self, obj):
        options = obj.options.all()
        ser = OptionSerializer(options, many=True)
        return ser.data

class QuizAddQuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    options = OptionSerializer(many=True)
