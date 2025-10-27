from django.shortcuts import render, redirect
import uuid
from crudRedis.settings import redis_client
from django.http import HttpResponse 
# Create your views here.

def index(request):
    return render(request, 'index.html')

# iterar por tarefas usando {% for tarefa in tarefas %}
# coletar informações com {{ tarefa.titulo }} etc...
# finalizar com {% endfor %}
def list(request):
    tarefas = []
    for id in redis_client.lrange('tarefas',0,-1):
        tarefa_id = 'tarefa:'+str(id)
        detalhes = {
            'titulo':redis_client.hget(tarefa_id,'titulo'),
            'descricao':redis_client.hget(tarefa_id,'descricao'),
            'data':redis_client.hget(tarefa_id,'data'),
            'status':redis_client.hget(tarefa_id,'status'),
            'id':redis_client.hget(tarefa_id,'id')
            }
        tarefas.append(detalhes)
    return render(request, 'list.html', context={'tarefas':tarefas})

# <from action="{% url 'addTarefa' %}" method="post" ...> {% csrf_token %}
# <input> devem ter name igual aos valores em "POST.get('x')"
def add(request):
    if request.method == 'POST':
        id = uuid.uuid4().int
        tarefa_id = 'tarefa:'+str(id)
        redis_client.hset(tarefa_id,'id',id)
        redis_client.hset(tarefa_id,'titulo',request.POST.get('titulo'))
        redis_client.hset(tarefa_id,'descricao',request.POST.get('descricao'))
        redis_client.hset(tarefa_id,'data',request.POST.get('data'))
        redis_client.hset(tarefa_id,'status',request.POST.get('status'))
        redis_client.rpush('tarefas',id)
        return redirect('addTarefa')

    return render(request, 'add.html')

# adicionar <button> ou <a> com href="{% url 'updateTarefa' tarefa.id %}"
def update(request, id):
    tarefa_id = 'tarefa:'+str(id)
    if request.method == 'POST':
        redis_client.hset(tarefa_id,'titulo',request.POST.get('titulo'))
        redis_client.hset(tarefa_id,'descricao',request.POST.get('descricao'))
        redis_client.hset(tarefa_id,'data',request.POST.get('data'))
        redis_client.hset(tarefa_id,'status',request.POST.get('status'))
        return redirect('listTarefas')

    return render(request, 'update.html', {'tarefa_id':id})

# adicionar <button> ou <a> com href="{% url 'removeTarefa' tarefa.id %}"
def delete(request, id):
    tarefa_id = 'tarefa:'+str(id)
    redis_client.delete(tarefa_id)
    redis_client.lrem('tarefas',0,id)
    return redirect('listTarefas')