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
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

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
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }
        
class QuestionReadSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'text', 'options']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }
    def get_options(self, obj):
        options = obj.options.all()
        ser = OptionSerializer(options, many=True)
        return ser.data

class QuizAddQuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    options = OptionSerializer(many=True)

class QuizRemoveQuestionsSerializer(serializers.Serializer):
    questions_id = serializers.PrimaryKeyRelatedField(
        queryset = Question.objects.all(),
        many = True
    )

class AddStudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()