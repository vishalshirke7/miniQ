from .models import User


def add_variable_to_context(request):
    if 'user_id' in request.session:
        userid = request.session['user_id']
        user = User.objects.get(pk=userid)
        return {
            'logged_in': True,
            'user': user
        }
    return {
        'logged_in': False
    }
