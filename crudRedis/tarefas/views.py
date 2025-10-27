from django.shortcuts import render, redirect
import uuid
from crudRedis.settings import redis_client


# Entry point: redirect to tarefas list
def index(request):
    return redirect('listTarefas')


# List all tarefas
def list(request):
    tarefas = []
    for id in redis_client.lrange('tarefas', 0, -1):
        tarefa_id = 'tarefa:' + str(id)
        detalhes = {
            'titulo': redis_client.hget(tarefa_id, 'titulo'),
            'descricao': redis_client.hget(tarefa_id, 'descricao'),
            'data': redis_client.hget(tarefa_id, 'data'),
            'status': redis_client.hget(tarefa_id, 'status'),
            'id': redis_client.hget(tarefa_id, 'id')
        }
        tarefas.append(detalhes)
    return render(request, 'tarefas/list.html', context={'tarefas': tarefas})


# Create a new tarefa
def add(request):
    if request.method == 'POST':
        id = uuid.uuid4().int
        tarefa_id = 'tarefa:' + str(id)
        redis_client.hset(tarefa_id, 'id', id)
        redis_client.hset(tarefa_id, 'titulo', request.POST.get('titulo'))
        redis_client.hset(tarefa_id, 'descricao', request.POST.get('descricao'))
        redis_client.hset(tarefa_id, 'data', request.POST.get('data'))
        redis_client.hset(tarefa_id, 'status', request.POST.get('status') or 'pendente')
        redis_client.rpush('tarefas', id)
        return redirect('listTarefas')

    return render(request, 'tarefas/add.html')


# Update an existing tarefa
def update(request, id):
    tarefa_id = 'tarefa:' + str(id)
    if request.method == 'POST':
        redis_client.hset(tarefa_id, 'titulo', request.POST.get('titulo'))
        redis_client.hset(tarefa_id, 'descricao', request.POST.get('descricao'))
        redis_client.hset(tarefa_id, 'data', request.POST.get('data'))
        redis_client.hset(tarefa_id, 'status', request.POST.get('status'))
        return redirect('listTarefas')

    detalhes = {
        'titulo': redis_client.hget(tarefa_id, 'titulo'),
        'descricao': redis_client.hget(tarefa_id, 'descricao'),
        'data': redis_client.hget(tarefa_id, 'data'),
        'status': redis_client.hget(tarefa_id, 'status'),
        'id': redis_client.hget(tarefa_id, 'id')
    }
    return render(request, 'tarefas/update.html', {'tarefa': detalhes})


# Confirm and delete a tarefa
def delete(request, id):
    tarefa_id = 'tarefa:' + str(id)
    if request.method == 'POST':
        redis_client.delete(tarefa_id)
        redis_client.lrem('tarefas', 0, id)
        return redirect('listTarefas')

    detalhes = {
        'titulo': redis_client.hget(tarefa_id, 'titulo'),
        'id': redis_client.hget(tarefa_id, 'id')
    }
    return render(request, 'tarefas/confirm_delete.html', {'tarefa': detalhes})