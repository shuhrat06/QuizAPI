from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsAdminUser, IsTeacherUser
from rest_framework.permissions import IsAuthenticated

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
    QuestionReadSerializer
)

class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [(IsAdminUser | IsTeacherUser)()]

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
    permission_classes = [IsAdminUser | IsTeacherUser]

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
