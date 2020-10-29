from counter.models import Action, Count
import sqlite3

conn = sqlite3.connect('../../db.sqlite3')
cursor = conn.cursor()

counts = cursor.execute("select * from bizint_count").fetchall()
actions = cursor.execute("select * from bizint_action").fetchall()

action_dict = {}

for action in actions:
    action_id, action_name, date_created = action
    Action.objects.create(name=action_name, creation_date=date_created)
    action_dict[action_id] = action_name


for count in counts:
    _, count_count, action_id, week, date = count
    Count.objects.create(count=count_count, action=Action.objects.get(name=action_dict[action_id]), update_date=date, update_week=week)