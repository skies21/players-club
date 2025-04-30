from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('director', 'Директор'),
        ('coach', 'Тренер'),
        ('guest', 'Гость'),
    )
    role = models.CharField(max_length=64, choices=ROLE_CHOICES, default='guest')

    def is_director(self):
        return self.role == 'director'

    def is_coach(self):
        return self.role == 'coach'

    def is_guest(self):
        return self.role == 'guest'


class Position(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Player(models.Model):
    INJURY_CHOICES = (
        ('', '—'),
        ('да', 'ДА'),
        ('нет', 'НЕТ'),
    )

    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=0)
    position = models.ForeignKey(to=Position, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField(default='2031-01-01')
    injury_choice = models.CharField(max_length=20, choices=INJURY_CHOICES, default='Нет')
    injury_date = models.DateField(blank=True, null=True)
    recovery_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return f' {self.surname} {self.firstname} {self.patronymic}'


class FullName(models.Model):
    full_name = models.ForeignKey(to=Player, on_delete=models.CASCADE)


    def __str__(self):
        return self.full_name


class Medcine(models.Model):
    full_name = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    injury = models.CharField(max_length=40)
    injury_date = models.DateField(blank=True, null=True)
    recovery_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}. Травма: {self.injury}. Дата получения травмы: {self.injury_date}. Дата выздоровления: {self.recovery_date}."


MONTH_CHOICES = [(i, datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]

class FinanceEntry(models.Model):
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTH_CHOICES)

    # Доходы
    match_income = models.PositiveIntegerField(default=0)
    sponsors_income = models.PositiveIntegerField(default=0)
    transfers_income = models.PositiveIntegerField(default=0)
    prize_income = models.PositiveIntegerField(default=0)
    merch_income = models.PositiveIntegerField(default=0)
    other_income = models.PositiveIntegerField(default=0)

    # Расходы
    transfers_expense = models.PositiveIntegerField(default=0)
    salary_expense = models.PositiveIntegerField(default=0)
    academy_expense = models.PositiveIntegerField(default=0)
    infra_expense = models.PositiveIntegerField(default=0)
    merch_expense = models.PositiveIntegerField(default=0)

    @property
    def total_income(self):
        return (self.match_income + self.sponsors_income + self.transfers_income +
                self.prize_income + self.merch_income + self.other_income)

    @property
    def total_expense(self):
        return (self.transfers_expense + self.salary_expense +
                self.academy_expense + self.infra_expense + self.merch_expense)

    @property
    def profit(self):
        return self.total_income - self.total_expense

    class Meta:
        unique_together = ('year', 'month')
        ordering = ['year', 'month']


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/')

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Comment on {self.news.title} by {self.user.username if self.user else 'Anonymous'}"
