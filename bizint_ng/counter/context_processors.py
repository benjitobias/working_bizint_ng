from guardian.shortcuts import get_objects_for_user
from django.contrib.auth.models import User


def get_user_actions(request):
    user = request.user

    if not user.is_authenticated:
        actions = None
    else:
        actions = get_objects_for_user(user, 'counter.view_action')
    return {'actions': actions}
