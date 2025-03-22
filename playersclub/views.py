from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages

from users.forms import PlayerForm, EditForm, EditPositionForm, PositionForm, MedcineForm
from users.models import Player, Position, Medcine, FullName

class IndexView(TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Player.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})

class SearchView(View):
    template_name = 'users/search.html'
    results_template_name = 'users/search_result.html'

    def get(self, request, *args, **kwargs):
        form = PlayerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PlayerForm(request.POST)

        if form.is_valid():
            search_results = Player.objects.all()

            if form.cleaned_data['surname']:
                search_results = search_results.filter(surname=form.cleaned_data['surname'])

            if form.cleaned_data['firstname']:
                search_results = search_results.filter(firstname=form.cleaned_data['firstname'])

            if form.cleaned_data['patronymic']:
                search_results = search_results.filter(patronymic=form.cleaned_data['patronymic'])

            if form.cleaned_data['position']:
                search_results = search_results.filter(position__name=form.cleaned_data['position'])

            if form.cleaned_data['age']:
                search_results = search_results.filter(age=form.cleaned_data['age'])

            if form.cleaned_data['cost']:
                search_results = search_results.filter(cost=form.cleaned_data['cost'])

            if form.cleaned_data['expiration_date']:
                search_results = search_results.filter(expiration_date=form.cleaned_data['expiration_date'])

            if form.cleaned_data['injury_choice']:
                search_results = search_results.filter(expiration_date=form.cleaned_data['injury_choice'])

            if form.cleaned_data['injury_date']:
                search_results = search_results.filter(expiration_date=form.cleaned_data['injury_date'])

            if form.cleaned_data['recovery_date']:
                search_results = search_results.filter(expiration_date=form.cleaned_data['recovery_date'])

            if not search_results.exists():
                return render(request, self.results_template_name, {'no_results': True})

            return render(request, self.results_template_name, {'results': search_results})

        return render(request, self.template_name, {'form': form})

class AddRecordView(View):
    template_name = 'users/add_record.html'
    success_url = 'users/index.html'

    def get(self, request):
        form = PlayerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PlayerForm(request.POST)
        if form.is_valid():
            # Проверяем и создаем новые значения в соответствующих таблицах, если они отсутствуют
            fields_to_check = ['position']
            for field in fields_to_check:
                value = form.cleaned_data[field]
                model_class = globals()[field.capitalize()]
                model_class.objects.get_or_create(name=value)

            # Создаем запись в основной таблице
            main_fields = {
                'firstname': form.cleaned_data['firstname'],
                'surname': form.cleaned_data['surname'],
                'patronymic': form.cleaned_data['patronymic'],
                'position': Position.objects.get(name=form.cleaned_data['position']),
                'age': form.cleaned_data['age'],
                'cost': form.cleaned_data['cost'],
                'expiration_date': form.cleaned_data['expiration_date'],
                'injury_choice': form.cleaned_data['injury_choice'],
                'injury_date': form.cleaned_data['injury_date'],
                'recovery_date': form.cleaned_data['recovery_date']
            }
            Player.objects.create(**main_fields)

            return redirect('index')
        return render(request, self.template_name, {'form': form})

class EditRecordView(UpdateView):
    template_name = 'users/edit_record.html'
    model = Player
    form_class = EditForm
    success_message = 'Запись обновлена!'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return get_object_or_404(Player, pk=self.kwargs['pk'])


def delete_record(request, pk):
    record = Player.objects.get(pk=pk)
    record.delete()
    return redirect('index')

class IndexPositionView(TemplateView):
    template_name = 'users/position.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Position.objects.all()
        return context


def delete_record_position(request, pk):
    record = Position.objects.get(pk=pk)
    record.delete()
    return redirect('position')

class EditRecordPositionView(UpdateView):
    template_name = 'users/edit_record_position.html'
    model = Position
    form_class = EditPositionForm
    success_message = 'Запись обновлена!'
    success_url = reverse_lazy('position')

    def get_object(self, queryset=None):
        return get_object_or_404(Position, pk=self.kwargs['pk'])

class AddRecordPositionView(View):
    template_name = 'users/add_record_position.html'
    succsess_url = 'users/position.html'

    def get(self, request):
        form = PositionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PositionForm(request.POST)
        if form.is_valid():
            # Проверяем и создаем новые значения в соответствующих таблицах, если они отсутствуют
            position = form.cleaned_data['name']

            # Surname.objects.get_or_create(name=surname)

            # Создаем запись в таблице фамилий
            Position.objects.create(name=position)

            return redirect('position')
        return render(request, self.template_name, {'form': form})

class HomeView(View):
    template_name = 'users/home.html'
    def get(self, request):
        return render(request, 'users/home.html')

class MedcineView(TemplateView):
    template_name = 'users/medcine.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Player.objects.filter(injury_choice='да')
        return context

    def post(self, request, *args, **kwargs):
        form = MedcineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})

class AddRecordMedcineView(View):
    template_name = 'users/add_record_medcine.html'
    success_url = 'users/medcine.html'

    def get(self, request):
        form = MedcineForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MedcineForm(request.POST)
        if form.is_valid():
            # Проверяем и создаем новые значения в соответствующих таблицах, если они отсутствуют
            fields_to_check = ['full_name']
            for field in fields_to_check:
                value = form.cleaned_data[field]
                model_class = globals()[field.capitalize()]
                model_class.objects.get_or_create(name=value)

            # Создаем запись в основной таблице
            main_fields = {
                'full_name': FullName.objects.get(name=form.cleaned_data['full_name']),
                'injury': form.cleaned_data['injury'],
                'injury_date': form.cleaned_data['injury_date'],
                'recovery_date': form.cleaned_data['recovery_date'],
            }
            Medcine.objects.create(**main_fields)

            return redirect('medcine')
        return render(request, self.template_name, {'form': form})

class EditRecordMedcineView(UpdateView):
    template_name = 'users/edit_record_medcine.html'
    model = Medcine
    form_class = EditForm
    success_message = 'Запись обновлена!'
    success_url = reverse_lazy('medcine')

    def get_object(self, queryset=None):
        return get_object_or_404(Medcine, pk=self.kwargs['pk'])


def delete_record_medcine(request, pk):
    record = Medcine.objects.get(pk=pk)
    record.delete()
    return redirect('medcine')

'''class FinancesView(TemplateView):
    template_name = 'users/finances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Player.objects.all
        return context

    def post(self, request, *args, **kwargs):
        form = FinancesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})'''


def calculate_total_cost():
    total_cost = Player.objects.aggregate(total_cost=Sum('cost'))['total_cost']
    return total_cost

class FinancesView(View):
    template_name = 'users/finances.html'

    def get(self, request):
        total_cost = calculate_total_cost()
        context = {
            'total_cost': total_cost
        }
        return render(request, 'users/finances.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Такого пользователя не существует и/или пароль неверный")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users/home.html')
        else:
            messages.error(request, "Такого пользователя не существует и/или пароль неверный")
    context = {}
    return render(request, 'users/login.html', context)


def registerPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('users/login.html')

    else:
        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'users/register-page.html', context)

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')