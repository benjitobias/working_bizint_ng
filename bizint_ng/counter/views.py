from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import generic
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403

from .models import Action


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
    count = action.get_count()
    return render(request, 'counter/info.html', {'action': action, 'count': count})


@permission_required_or_403('counter.change_action', (Action, 'id', 'action_id'))
def add(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    action.count_set.create(count=action.get_count() + 1)
    return HttpResponse(action.get_count())
