# athletes/models.py
from django.db import models

class Athlete(models.Model):
	SPORT_CHOICES = [
		('football', 'Футбол'),
		('basketball', 'Баскетбол'),
		('tennis', 'Теннис'),
		('swimming', 'Плавание'),
		('athletics', 'Легкая атлетика'),
	]

	name = models.CharField(max_length=100, verbose_name='Имя')
	surname = models.CharField(max_length=100, verbose_name='Фамилия')
	age = models.PositiveIntegerField(verbose_name='Возраст')
	sport = models.CharField(max_length=50, choices=SPORT_CHOICES, verbose_name='Вид спорта')
	achievements = models.TextField(verbose_name='Достижения')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Спортсмен'
		verbose_name_plural = 'Спортсмены'

	def __str__(self):
		return f"{self.name} {self.surname}"