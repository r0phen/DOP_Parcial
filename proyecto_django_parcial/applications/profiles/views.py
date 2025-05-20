from django.shortcuts import render
from applications.auth.models import User, FavoriteGame

def profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'profiles/profile.html', {
            'user': None,
            'favorite_games': []
        })

    user = User.objects.get(id=user_id)
    favorites = FavoriteGame.objects.filter(user=user)

    return render(request, 'profiles/profile.html', {
        'user': user,
        'favorite_games': favorites,
        'show_button': False
    })
