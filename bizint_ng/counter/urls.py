from django.urls import path
from . import views

app_name = 'counter'

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('<int:action_id>/', views.info, name='info'),
    path('<int:action_id>/add', views.add, name='add'),
    #TODO: remove from here, will be in info
    path('populate-actions-chart/', views.populate_actions_chart, name='populate_actions_chart'),
]