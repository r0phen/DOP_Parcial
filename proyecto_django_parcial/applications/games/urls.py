from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('<int:game_id>/add_favorite/', views.add_favorite, name='add_favorite'),
    path('delete_favorite/<int:favorite_id>/', views.delete_favorite, name='delete_favorite'),
]
