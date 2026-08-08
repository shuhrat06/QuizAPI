from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsAdminUser, IsTeacherUser
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny

from drf_yasg.utils import swagger_auto_schema

from .models import (
    Quiz,
    Question,
    Option
)
from .serializers import (
    QuizCreateSerializer,
    QuizDetailSerializer,
    QuizUpdateSerializer,
    QuizAddQuestionSerializer,
    OptionSerializer,
    QuestionReadSerializer,
    QuestionSerializer,
    QuizRemoveQuestionsSerializer,
)

from .permissions import IsOwnerofQuiz, IsOwnerofQuestion, IsOwnerofOption


class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create']:
            return [(IsAdminUser | IsTeacherUser)()]
        return [(IsAdminUser | IsOwnerofQuiz)()]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return QuizDetailSerializer
        elif self.action == 'create':
            return QuizCreateSerializer
        return QuizUpdateSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data.pop('allowed_students')
        return response
        
class QuizAddQuestionApiView(APIView):
    permission_classes = [IsAdminUser | IsOwnerofQuiz]

    @swagger_auto_schema(
        operation_description="Add question to quiz",
        request_body=QuizAddQuestionSerializer
    )
    def post(self, request, pk):
        data = request.data.copy()
        quiz = get_object_or_404(Quiz, id=pk)
        question = Question.objects.create(
            quiz=quiz,
            text = data['text']
        )
        options = [
            Option(
                question=question,
                text = op_data['text'],
                is_correct = op_data['is_correct']
            ) for op_data in data['options']
        ]
        Option.objects.bulk_create(options)
        return Response(status=200)

class QuizRemoveQuestionsApiView(APIView):
    permission_classes = [IsAdminUser | IsOwnerofQuiz]
    @swagger_auto_schema(
        operation_description="Quizdan savollarni o'chirish",
        request_body=QuizRemoveQuestionsSerializer
    )
    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, id=pk)
        ser = QuizRemoveQuestionsSerializer(data = request.data)
        ser.is_valid(raise_exception=True)
        questions = ser.validated_data['questions_id']
        quiz.questions.filter(id__in=[q.id for q in questions]).delete()
        return Response(status=200)
        
class QuizQuestionsListApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = QuestionReadSerializer
    pagination_class = None
    def get_queryset(self):
        quiz_id = self.kwargs.get("pk")
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return quiz.questions.all()

class QuestionRetrieveApiView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [(IsAdminUser | IsOwnerofQuestion)()]

class OptionRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [(IsAdminUser | IsOwnerofOption)()]
