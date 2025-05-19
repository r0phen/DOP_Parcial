import requests
from django.shortcuts import render

def games_list(request):
    # Parámetros disponibles
    platform = request.GET.get('platform', 'all')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort_by', 'release-date')
    
    # Construir la URL de la API según los filtros
    base_url = "https://www.freetogame.com/api/games"
    params = {}
    
    if platform and platform != 'all':
        params['platform'] = platform
    
    if category:
        params['category'] = category
    
    if sort_by:
        params['sort-by'] = sort_by
    
    # Hacer la solicitud a la API
    response = requests.get(base_url, params=params)
    games = response.json() if response.status_code == 200 else []
    
    # Opciones para los dropdowns
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
    }
    
    return render(request, 'games/games_list.html', context)