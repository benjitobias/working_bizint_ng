import datetime
from counter.models import Action, Count
import sqlite3
import pytz

conn = sqlite3.connect('old_db.sqlite3')
cursor = conn.cursor()

counts = cursor.execute("select * from bizint_count").fetchall()
actions = cursor.execute("select * from bizint_action").fetchall()

action_dict = {}

for action in actions:
    action_id, action_name, date_created = action
    try:
        date_created = datetime.datetime.strptime(date_created, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        date_created = datetime.datetime.strptime(date_created, '%Y-%m-%d %H:%M:%S')

    date_created = pytz.utc.localize(date_created)

    Action.objects.create(name=action_name, creation_date=date_created)
    action_dict[action_id] = action_name


for count in counts:
    _, count_count, action_id, week, date = count
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date = pytz.utc.localize(date)
    Count.objects.create(count=count_count, action=Action.objects.get(name=action_dict[action_id]), update_date=date, update_week=week)