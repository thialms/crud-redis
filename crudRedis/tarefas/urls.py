from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('tarefas', views.list, name='listTarefas'),
    path('addTarefa', views.add, name='addTarefa'),
    path('updateTarefa/<str:id>', views.update, name='updateTarefa'),
    path('removeTarefa/<str:id>', views.delete, name='removeTarefa'),
]