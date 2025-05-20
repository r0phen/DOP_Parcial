from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from applications.auth.models import User, FavoriteGame
import requests

def games_list(request):
    platform = request.GET.get('platform', 'all')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort_by', 'release-date')

    base_url = "https://www.freetogame.com/api/games"
    params = {}

    if platform and platform != 'all':
        params['platform'] = platform

    if category:
        params['category'] = category

    if sort_by:
        params['sort-by'] = sort_by

    response = requests.get(base_url, params=params)
    games = response.json() if response.status_code == 200 else []

    platforms = [
        {'value': 'all', 'label': 'Todas las plataformas'},
        {'value': 'pc', 'label': 'PC'},
        {'value': 'browser', 'label': 'Navegador'},
    ]

    categories = [
        {'value': '', 'label': 'Todas las categorías'},
        {'value': 'mmorpg', 'label': 'MMORPG'},
        {'value': 'shooter', 'label': 'Shooter'},
        {'value': 'strategy', 'label': 'Estrategia'},
        {'value': 'moba', 'label': 'MOBA'},
        {'value': 'racing', 'label': 'Carreras'},
        {'value': 'sports', 'label': 'Deportes'},
        {'value': 'social', 'label': 'Social'},
        {'value': 'sandbox', 'label': 'Sandbox'},
    ]

    sort_options = [
        {'value': 'release-date', 'label': 'Fecha de lanzamiento'},
        {'value': 'popularity', 'label': 'Popularidad'},
        {'value': 'alphabetical', 'label': 'Orden alfabético'},
        {'value': 'relevance', 'label': 'Relevancia'},
    ]

    context = {
        'games': games,
        'platforms': platforms,
        'categories': categories,
        'sort_options': sort_options,
        'current_platform': platform,
        'current_category': category,
        'current_sort': sort_by,
        'show_button': True,
    }

    return render(request, 'games/games_list.html', context)


def game_detail(request, game_id):
    url = f"https://www.freetogame.com/api/game?id={game_id}"
    response = requests.get(url)
    game = response.json() if response.status_code == 200 else None

    user_id = request.session.get('user_id')
    is_logged_in = user_id is not None

    return render(request, 'games/game_detail.html', {
        'game': game,
        'is_logged_in': is_logged_in,
    })


@require_POST
def add_favorite(request, game_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('auth:login')

    user = User.objects.get(id=user_id)
    url = f"https://www.freetogame.com/api/game?id={game_id}"
    response = requests.get(url)

    if response.status_code == 200:
        game = response.json()
        if not FavoriteGame.objects.filter(user=user, game_id=game_id).exists():
            FavoriteGame.objects.create(
                user=user,
                game_id=game['id'],
                title=game['title'],
                description=game['short_description'],
                thumbnail=game['thumbnail'],
            )

    return redirect('games:game_detail', game_id=game_id)


@require_POST
def delete_favorite(request, favorite_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('auth:login')

    try:
        favorite = FavoriteGame.objects.get(id=favorite_id, user_id=user_id)
        favorite.delete()
    except FavoriteGame.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para eliminar este favorito.")

    return redirect('profiles:profile')  # Cambia el namespace si usas otro para el perfil
