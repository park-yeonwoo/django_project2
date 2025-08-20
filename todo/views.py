from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from todo.forms import TodoForm, TodoUpdateForm
from todo.models import Todo

# Create your views here.

@login_required()
def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).order_by('created_at')
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(Q(title__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'todo/todo_list.html', context)

@login_required()
def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    context = {
        'todo': todo.__dict__
    }

    return render(request, 'todo/todo_info.html', context)

@login_required()
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs= {'todo_id': todo.pk}))
    context = {
        'form': form
    }
    return render(request, 'todo.todo_create.html', context)

@login_required()
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id= todo_id, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        """
        return redirect(reverse('todo_list'kwargs={'todo_id': todo.pk})) 
        실행 시 NoReverseMatch error 발생! / GPT 에게 이유를 물어보니 todo_id라는 파라미터가 존재하지 않아 발생한 에러라고 함
        todo_id : todo.pk 지우니 괜찮아짐!
        ㄴ 파라미터가 없어 URL을 찾지 못함
        ㄴ현재는 단순 todo 구조여서 뒤에만 지우면 괜찮아짐! 
        """
        return redirect(reverse('todo_list'))
    context = {
        'form': form
    }
    return render(request, 'todo/todo_update.html', context)

@login_required()
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id= todo_id, user= request.user)
    todo.delete()
    return redirect(reverse('todo_list'))