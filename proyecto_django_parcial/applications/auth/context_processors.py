from .models import User

def auth_user(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
    return {
        'auth_user': user,
        'is_authenticated': user is not None,
    }
