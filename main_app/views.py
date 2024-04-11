import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game, Platform, Photo
from .forms import PlayingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def games_index(request):
  games = Game.objects.filter(user=request.user)

  return render(request, 'games/index.html', {
    'games': games
  })

@login_required
def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  
  id_list = game.platforms.all().values_list('id')

  platforms_game_doesnt_have = Platform.objects.exclude(id__in=id_list)

  playing_form = PlayingForm()
  return render(request, 'games/detail.html', {
    'game': game, 'playing_form': playing_form,
    'platforms': platforms_game_doesnt_have
  })

class GameCreate(LoginRequiredMixin, CreateView):
  model = Game
  fields = ['name', 'genre', 'description']

  def form_valid(self, form):
    # self.request.user is the logged in user
    form.instance.user = self.request.user
    # Let the CreateView's form_valid method
    # do its regular work (saving the object & redirecting)
    return super().form_valid(form)


class GameUpdate(LoginRequiredMixin, UpdateView):
  model = Game
  fields = ['genre', 'description']

class GameDelete(LoginRequiredMixin, DeleteView):
  model = Game
  success_url = '/games'

@login_required
def add_playing(request, game_id):
  
  form = PlayingForm(request.POST)

  if form.is_valid():
  
    new_playing = form.save(commit=False)
    new_playing.game_id = game_id
    new_playing.save()
  return redirect('detail', game_id=game_id)

class PlatformList(LoginRequiredMixin, ListView):
  model = Platform

class PlatformDetail(LoginRequiredMixin, DetailView):
  model = Platform

class PlatformCreate(LoginRequiredMixin, CreateView):
  model = Platform
  fields = '__all__'

class PlatformUpdate(LoginRequiredMixin, UpdateView):
  model = Platform
  fields = ['name']

class PlatformDelete(LoginRequiredMixin, DeleteView):
  model = Platform
  success_url = '/platforms'

@login_required
def assoc_platform(request, game_id, platform_id):
  Game.objects.get(id=game_id).platforms.add(platform_id)
  return redirect('detail', game_id=game_id)

@login_required
def unassoc_platform(request, game_id, platform_id):
  Game.objects.get(id=game_id).platforms.remove(platform_id)
  return redirect('detail', game_id=game_id)

@login_required
def add_photo(request, game_id):
  # photo-file maps to the "name" attr on the <input>
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # Need a unique "key" (filename)
    # It needs to keep the same file extension
    # of the file that was uploaded (.png, .jpeg, etc.)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, game_id=game_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', game_id=game_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)