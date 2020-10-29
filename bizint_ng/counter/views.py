from django.shortcuts import render, get_object_or_404
from django.views import generic
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403
from django.db.models import Count as CountFunction
from django.http import JsonResponse
from guardian.shortcuts import get_objects_for_user

from .models import Action, Count


class IndexView(generic.ListView):
    template_name = 'counter/index.html'
    context_object_name = 'action_list'

    def get_queryset(self):
        #return Action.objects.all()
        return get_objects_for_user()


def index(request):
    return render(request, 'counter/index.html')


@permission_required_or_403('counter.view_action', (Action, 'id', 'action_id'))
def info(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    return render(request, 'counter/info.html', {'action': action})


@permission_required_or_403('counter.change_action', (Action, 'id', 'action_id'))
def add(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    action.count_set.create(count=action.get_count() + 1)

    return render(request, 'counter/info.html', {'action': action})


#TODO: implement into info
def populate_actions_chart(request):
    labels = []
    data = []
    if request.user.is_authenticated:
        actions = get_objects_for_user(request.user, 'counter.view_action')

        for action in actions:
            labels.append(action.name)
            data.append(action.get_count())

        data = {
            'labels': labels,
            'data': data
        }
    return JsonResponse(data=data)
