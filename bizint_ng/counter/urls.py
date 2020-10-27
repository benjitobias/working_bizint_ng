from django.urls import path
from . import views

app_name = 'counter'

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('<int:action_id>/', views.info, name='info'),
    path('<int:action_id>/add', views.add, name='add'),
]