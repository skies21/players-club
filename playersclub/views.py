from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import TemplateView
from django.contrib import messages

from users.forms import PlayerForm, EditForm, EditPositionForm, PositionForm, MedcineForm, RegisterForm
from users.models import Player, Position, Medcine


class IndexView(UserPassesTestMixin, TemplateView):
    template_name = 'users/index.html'
    success_url = 'users/index.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_director() or self.request.user.is_coach()

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

class SearchView(UserPassesTestMixin, View):
    template_name = 'users/search.html'
    results_template_name = 'users/search_result.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_director() or self.request.user.is_coach()

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

class IndexPositionView(UserPassesTestMixin, TemplateView):
    template_name = 'users/position.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_director() or self.request.user.is_coach()

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


class MedcineView(UserPassesTestMixin, TemplateView):
    template_name = 'users/medcine.html'
    success_url = 'users/medcine.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_director() or self.request.user.is_coach()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Medcine.objects.all()
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

    def get(self, request):
        form = MedcineForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MedcineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно добавлена!")
            return redirect(reverse_lazy('medcine'))
        return render(request, self.template_name, {'form': form})


class EditRecordMedcineView(UpdateView):
    model = Medcine
    form_class = MedcineForm
    template_name = 'users/edit_record_medcine.html'
    success_url = reverse_lazy('medcine')
    success_message = 'Запись успешно обновлена!'


class DeleteRecordMedcineView(View):
    def get(self, request, pk):
        record = get_object_or_404(Medcine, pk=pk)
        record.delete()
        return redirect(reverse_lazy('medcine'))


def calculate_total_cost():
    total_cost = Player.objects.aggregate(total_cost=Sum('cost'))['total_cost']
    return total_cost


class FinancesView(UserPassesTestMixin, View):
    template_name = 'users/finances.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_director()

    def get(self, request):
        total_cost = calculate_total_cost()
        context = {
            'total_cost': total_cost
        }
        return render(request, 'users/finances.html', context)


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("home")
        else:
            messages.error(request, "Ошибка регистрации. Проверьте данные.")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли!")
            return redirect("home")
        else:
            messages.error(request, "Ошибка входа. Проверьте логин и пароль.")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect("home")
