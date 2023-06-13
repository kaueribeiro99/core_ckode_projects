from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'  # Uso essa classe para renomear as tabelas do meu BD


class Lead(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'leads'  # Uso essa classe para renomear as tabelas do meu BD


class Project(models.Model):
    STATUS_CHOICES = [
        (1, 'In Progress'),
        (2, 'Finished'),
        (3, 'Closed'),
        (4, 'Proposal'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.PROTECT)  # Não deixo apagar o Lead se estiver Project vinculado.
    name = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    value = models.FloatField()
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'projects'  # Uso essa classe para renomear as tabelas do meu BD
