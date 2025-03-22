from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=128)


    def __str__(self):
        return self.name


injury_choices = (
    ('да', 'ДА'),
    ('нет', 'НЕТ'),
)


class Player(models.Model):
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=0)
    position = models.ForeignKey(to=Position, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField(default='2031-01-01')
    injury_choice = models.CharField(max_length=20, choices=injury_choices, default='Нет')
    injury_date = models.DateField()
    recovery_date = models.DateField()


    def __str__(self):
        return f' {self.surname} {self.firstname} {self.patronymic}'


class FullName(models.Model):
    full_name = models.ForeignKey(to=Player, on_delete=models.CASCADE)


    def __str__(self):
        return self.full_name


class Medcine(models.Model):
    full_name = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    injury = models.CharField(max_length=40)
    injury_date = models.CharField(max_length=16, default='01.01.2031')
    recovery_date = models.CharField(max_length=16, default='01.01.2031')


    def __str__(self):
        return f"{self.full_name}. Травма: {self.injury}. Дата получения травмы: {self.injury_date}. Дата выздоровления: {self.recovery_date}."
