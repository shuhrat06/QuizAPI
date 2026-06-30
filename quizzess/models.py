from re import S
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    allowed_students = models.ManyToManyField(User, related_name='available_quizzes', limit_choices_to={'role': 'STUDENT'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} (by {self.created_by.username})"

class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.TextField()

    def __str__(self):
        return f"{self.quiz.id} | {self.text}"

class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        related_name='options'
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE,
        related_name="submissions"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="submissions"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.quiz.title}"

class StudentAnswer(models.Model):
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE,
        related_name = 'answers'
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
    )
    selected_option = models.ForeignKey(
        Option, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.submission.student.username} → {self.question.text} = {self.selected_option.text}"
