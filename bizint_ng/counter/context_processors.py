from guardian.shortcuts import get_objects_for_user


def get_user_actions(request):
    user = request.user
    actions = get_objects_for_user(user, 'counter.view_action')
    if len(actions) == 0:
        actions = None
    return {'actions': actions}
