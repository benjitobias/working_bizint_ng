from guardian.shortcuts import get_objects_for_user
from django.db.models import Count as DbCount


def get_user_actions(request):
    user = request.user

    if not user.is_authenticated:
        actions = None
    else:
        actions = get_objects_for_user(user, 'counter.view_action')
        actions = actions.annotate(count_count=DbCount('count')).order_by('-count_count')
    return {'actions': actions}
