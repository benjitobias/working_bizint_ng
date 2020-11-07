from django.shortcuts import render, get_object_or_404
from django.views import generic
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403
from django.db.models import Count as CountFunction
from django.http import JsonResponse
from guardian.shortcuts import get_objects_for_user

from .models import Action, Count
from .telegram_bot import update_telegram_channel


class IndexView(generic.ListView):
    template_name = 'counter/index.html'
    context_object_name = 'action_list'

    def get_queryset(self):
        return get_objects_for_user()


def index(request):
    return render(request, 'counter/index.html')


@permission_required_or_403('counter.view_action', (Action, 'id', 'action_id'))
def info(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    print(request.GET)
    return render(request, 'counter/info.html', {'action': action})


@permission_required_or_403('counter.change_action', (Action, 'id', 'action_id'))
def add(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    if request.method == 'POST':
        action.count_set.create(count=action.get_count() + 1)

        if request.POST.get('update_telegram'):
            update_telegram_channel(action)

    return render(request, 'counter/info.html', {'action': action})


# TODO: implement into info
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


def graphs(request):
    return render(request, 'counter/graphs.html')


def populate_graphs(request):
    from calendar import month_abbr
    if request.user.is_authenticated:
        actions = get_objects_for_user(request.user, 'counter.view_action')
    else:
        actions = ["Shit", "Fap", "Gym", "Shower"]

    data = dict()
    data['labels'] = month_abbr[1:]

    datasets = list()

    for action_name in actions:
        action_data = dict()
        action_data['data'] = list()
        action_data['fill'] = False
        action = Action.objects.get(name=action_name)
        action_data['label'] = action_name
        for month in range(1, 13):
            action_count = action.count_set.filter(update_date__year=2020, update_date__month=month).count()
            action_data['data'].append(action_count)

        datasets.append(action_data)

    data = {
        'labels': month_abbr[1:],
        'datasets': datasets
    }
    return JsonResponse(data=data)
