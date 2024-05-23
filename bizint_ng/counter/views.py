import csv

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403
from django.db.models import Count as CountFunction
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from guardian.shortcuts import get_objects_for_user
from calendar import month_abbr
from django.utils import timezone
from django.urls import reverse
from datetime import date, datetime
from zoneinfo import ZoneInfo

from .models import Action, Count
from .telegram_bot import update_telegram_channel

from .forms import CountForm

import tempfile


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
    form = CountForm()
    hide_add = False
    current_count = action.get_count()
    history = action.count_set.filter(count__lte=current_count).filter(count__gte=current_count - 10).values(
        'count', 'update_date', 'note', 'longitude', 'latitude')[::-1]

    latest_update_time = action.get_latest().update_date
    now = timezone.now()

    if (now - latest_update_time).seconds < 60:
        hide_add = True

    if request.method == 'POST':
        count_form = CountForm(request.POST)
        note = count_form['note'].value()
        longitude = count_form['longitude'].value()
        latitude = count_form['latitude'].value()
        tzinfo = count_form['timezone'].value()

        update_date = datetime.strptime(count_form['datetime'].value(), "%d/%m/%Y %H:%M:%S")
        update_date = update_date.replace(tzinfo=ZoneInfo(tzinfo))
        update_week = update_date.isocalendar()[1]
        action.count_set.create(count=action.get_count() + 1, note=note, longitude=longitude, latitude=latitude,
                                update_date=update_date, update_week=update_week)

        if request.POST.get('update_telegram'):
           update_telegram_channel(action)

        return redirect(reverse('counter:info', args=(action_id,)))

    return render(request, 'counter/info.html', {'action': action, 'form': form, 'hide_add': hide_add, 'history': history})


"""@permission_required_or_403('counter.change_action', (Action, 'id', 'action_id'))
def add(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    if request.method == 'POST':
        count_form = CountForm(request.POST)
        note = count_form['note'].value()
        longitude = count_form['longitude'].value()
        latitude = count_form['latitude'].value()
        action.count_set.create(count=action.get_count() + 1, note=note, longitude=longitude, latitude=latitude)
        print("redirect")
        print(reverse('counter:info', args=(action_id,)))
        return redirect(reverse('counter:info', args=(action_id,)))
        #action.count_set.create(count=action.get_count() + 1)

        #if request.POST.get('update_telegram'):
         #   update_telegram_channel(action)

    # return render(request, 'counter/info.html', {'action': action})
"""


"""@permission_required_or_403('counter.change_action', (Action, 'id', 'action_id'))
def add(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    if request.method == 'POST':
        action.count_set.create(count=action.get_count() + 1)

        if request.POST.get('update_telegram'):
            update_telegram_channel(action)

    return render(request, 'counter/info.html', {'action': action})
"""

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


def about(request):
    return render(request, 'counter/about.html')


def populate_graphs(request):
    try:
        currentYear = int(request.GET['currentYear'])
        currentMonth = int(request.GET['currentMonth'])
    except (KeyError, ValueError):
        currentYear = date.today().year
        currentMonth = date.today().month
    if request.user.is_authenticated:
        actions = [action.name for action in get_objects_for_user(request.user, 'counter.view_action')]
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
        for month in range(1, currentMonth + 1):
            action_count = action.count_set.filter(update_date__year=currentYear, update_date__month=month).count()
            action_data['data'].append(action_count)

        datasets.append(action_data)

    data = {
        'labels': month_abbr[1:],
        'datasets': datasets
    }
    return JsonResponse(data=data)


@permission_required_or_403('counter.view_action', (Action, 'id', 'action_id'))
def get_action_history(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    try:
        first = request.GET['first']
        last = request.GET['last']
        if first > last:
            first, last = last, first
        history = action.count_set.filter(count__lte=last).filter(count__gte=first).values('count', 'update_date', 'note', 'longitude', 'latitude')
        history = list(history)[::-1]
        print(history)
        return JsonResponse(history, safe=False)
    except KeyError:
        return JsonResponse({"error": "missing parameters"})
    except ValueError:
        return JsonResponse({"error": "invalid parameters"})


@permission_required_or_403('counter.view_action', (Action, 'id', 'action_id'))
def populate_action_graph(request, action_id):
    data = dict()
    data['labels'] = month_abbr[1:]

    datasets = list()

    action_data = dict()
    action_data['data'] = list()
    action_data['fill'] = False
    action = Action.objects.get(pk=action_id)
    action_data['label'] = action.name
    for month in range(1, 13):
        action_count = action.count_set.filter(update_date__year=2021, update_date__month=month).count()
        action_data['data'].append(action_count)
    datasets.append(action_data)

    data = {
        'labels': month_abbr[1:],
        'datasets': datasets
    }
    return JsonResponse(data=data)


@permission_required_or_403('counter.view_action', (Action, 'id', 'action_id'))
def generate_csv(request, action_id):
    action = Action.objects.get(pk=action_id)

    with tempfile.TemporaryFile(mode="w+") as tmp_file:
        csv_writer = csv.writer(tmp_file, delimiter=",")
        header = ['count', 'datetime', 'longitude', 'latitude', 'note']
        csv_writer.writerow(header)
        for instance in action.count_set.all():
            instance_count = instance.count
            update_datetime = instance.update_date.isoformat()
            longitude = instance.longitude
            latitude = instance.latitude
            note = instance.note
            data = [instance_count, update_datetime, longitude, latitude, note]
            csv_writer.writerow(data)

        tmp_file.seek(0)
        csv_data = tmp_file.read()

    response = HttpResponse(csv_data, content_type="text/csv")
    response['Content-Disposition'] = rf'inline; filename={action.name}.csv'
    return response



