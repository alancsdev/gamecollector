from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

games = [
    {'title': 'The Legend of Zelda: Breath of the Wild', 'genre': 'Action-Adventure', 'platform': 'Nintendo Switch', 'release_year': 2017},
    {'title': 'The Witcher 3: Wild Hunt', 'genre': 'Action-RPG', 'platform': 'Multi-platform', 'release_year': 2015},
    {'title': 'Red Dead Redemption 2', 'genre': 'Action-Adventure', 'platform': 'Multi-platform', 'release_year': 2018},
    {'title': 'God of War', 'genre': 'Action-Adventure', 'platform': 'PlayStation 4', 'release_year': 2018},
    {'title': 'Super Mario Odyssey', 'genre': 'Platformer', 'platform': 'Nintendo Switch', 'release_year': 2017}
]

TIMES = (
  ('A', '0m - 1h'),
  ('B', '1h - 3h'),
  ('C', '3h +'),
)


# Create your models here.
class Platform(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('platforms_detail', kwargs={'pk': self.id})


class Game(models.Model):
  name = models.CharField(max_length=100)
  genre = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  
  platforms = models.ManyToManyField(Platform)
  # add user_id FK column
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Changing this instance method
  # does not impact the database, therefore
  # no makemigrations is necessary
  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'game_id': self.id})

  def played_for_today(self):
    return self.playing_set.filter(date=date.today()).count() >= len(TIMES)


class Playing(models.Model):
  date = models.DateField('Playing Date')
  time = models.CharField(
    max_length=1,
    choices=TIMES,
    default=TIMES[0][0]
  )
  
  game = models.ForeignKey(
    Game,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"{self.get_time_display()} on {self.date}"

  class Meta:
    ordering = ['-date']


class Photo(models.Model):
  url = models.CharField(max_length=200)
  game = models.ForeignKey(Game, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for game_id: {self.game_id} @{self.url}"

