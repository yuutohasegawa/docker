from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Task
from .forms import TaskForm
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

class IndexView(View):
    def get(self, request):
        # タスクを取得し、completeフィールドで並べ替え
        todo_list = Task.objects.all().order_by('complete', 'start_date')
        
        context = {
            "todo_list": todo_list
        }

        # テンプレートをレンダリング
        return render(request, "mytodo/index.html", context)

class AddView(View):
    def get(self, request):
        form = TaskForm()
        # テンプレートのレンダリング処理
        return render(request, "mytodo/add.html", {'form': form})

    def post(self, request, *args, **kwargs):
        # 入力データをフォームに渡す
        form = TaskForm(request.POST)
        # 入力データに誤りがないかチェック
        if form.is_valid():
            # モデルに登録
            form.save()
            return redirect('/')
        
        # データが正常じゃない場合
        return render(request, 'mytodo/add.html', {'form': form})

class EditView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(instance=task)
        return render(request, 'mytodo/edit.html', {'form': form, 'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'mytodo/edit.html', {'form': form, 'task': task})

class UpdateTaskCompleteView(View):
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.complete = not task.complete
        task.save()
        return redirect('/')

@method_decorator(require_POST, name='dispatch')
class DeleteTaskView(View):
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('/')

# ビュークラスをインスタンス化
index = IndexView.as_view()
add = AddView.as_view()
edit = EditView.as_view()
update_task_complete = UpdateTaskCompleteView.as_view()
delete_task = DeleteTaskView.as_view()
