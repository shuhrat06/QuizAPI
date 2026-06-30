from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
        

class User(AbstractUser):
    class UserRoles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    role = models.CharField(
        max_length = 20,
        choices = UserRoles.choices,
        default = UserRoles.STUDENT
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="members"
    )

    def __str__(self):
        return f"{self.username} | {self.role}"

    def save(self, **kwargs):
        if self.is_superuser or self.is_staff:
            if self.role != 'admin':
                self.role = 'admin'
        return super().save(**kwargs)
