from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views import View
from django.db import transaction

from .models import Tasks
from .forms import PositionForm

class CustomLoginView(LoginView):
    template_name = 'base_todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base_todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'base_todo/task_list.html'
    context_object_name = 'tasks'
    queryset = Tasks.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context


class DetailTask(LoginRequiredMixin, DetailView):
    model = Tasks
    context_object_name = 'task'
    template_name = 'base_todo/task.html'


class CreateTask(LoginRequiredMixin ,CreateView):
    model = Tasks
    fields = ['title','description']
    success_url = reverse_lazy('tasks')
    template_name = 'base_todo/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Tasks
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'base_todo/task_form.html'


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Tasks
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'base_todo/task_delete.html'


class TaskReorder(View):

    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))