from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('games/', views.games_index, name='index'),
  path('games/<int:game_id>/', views.games_detail, name='detail'),
  path('games/create/', views.GameCreate.as_view(), name='games_create'),
  path('games/<int:pk>/update/', views.GameUpdate.as_view(), name='games_update'),
  path('games/<int:pk>/delete/', views.GameDelete.as_view(), name='games_delete'),
  path('games/<int:game_id>/add_playing/', views.add_playing, name='add_playing'),
  path('games/<int:game_id>/add_photo/', views.add_photo, name='add_photo'),
  path('games/<int:game_id>/assoc_platform/<int:platform_id>/', views.assoc_platform, name='assoc_platform'),
  path('games/<int:game_id>/unassoc_platform/<int:platform_id>/', views.unassoc_platform, name='unassoc_platform'),
  path('platforms/', views.PlatformList.as_view(), name='platforms_index'),
  path('platforms/<int:pk>/', views.PlatformDetail.as_view(), name='platforms_detail'),
  path('platforms/create/', views.PlatformCreate.as_view(), name='platforms_create'),
  path('platforms/<int:pk>/update/', views.PlatformUpdate.as_view(), name='platforms_update'),
  path('platforms/<int:pk>/delete/', views.PlatformDelete.as_view(), name='platforms_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]