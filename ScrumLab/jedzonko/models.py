from django.db import models
from django.urls import reverse

DAYS = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.CharField(max_length=255)
    recipe_description = models.CharField(max_length=255, default='-')
    # TODO: change description -> preparation
    description = models.CharField(max_length=1000)
    method_of_preparing = models.CharField(max_length=1000, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    preparation_time = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.name}, {self.votes}'


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    created = models.DateField(auto_now=True)
    recipes = models.ManyToManyField('Recipe', through='RecipePlan')

    def __str__(self) -> str:
        return f'{self.name}'


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=120)
    order = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day_name = models.ForeignKey('DayName', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.meal_name}, {self.recipe}, {self.plan}, {self.day_name}'


class DayName(models.Model):
    name = models.CharField(max_length=16, choices=DAYS)
    order = models.IntegerField(unique=True)  # kolejność dnia

    def __str__(self) -> str:
        return f'{self.name}, {self.order}'


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255)

