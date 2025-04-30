from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.generic.edit import UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import TemplateView
from django.contrib import messages

from users.forms import PlayerForm, EditForm, EditPositionForm, PositionForm, MedcineForm, RegisterForm, \
    FinanceEntryForm, CommentForm
from users.models import Player, Position, Medcine, FinanceEntry, News


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
        return self.request.user.is_authenticated and (self.request.user.is_director() or self.request.user.is_coach())

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

            injury_choice = form.cleaned_data['injury_choice']
            if injury_choice:
                if injury_choice != '':
                    search_results = search_results.filter(injury_choice=injury_choice)

            if form.cleaned_data['injury_date']:
                search_results = search_results.filter(injury_date=form.cleaned_data['injury_date'])

            if form.cleaned_data['recovery_date']:
                search_results = search_results.filter(recovery_date=form.cleaned_data['recovery_date'])

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
        news = News.objects.all().order_by('-published_at')
        return render(request, self.template_name, {'news_list': news})


class NewsDetailView(View):
    template_name = 'users/news_detail.html'

    def get(self, request, pk):
        news_item = get_object_or_404(News, pk=pk)
        comments = news_item.comments.all()
        form = CommentForm()
        return render(request, self.template_name, {'news_item': news_item, 'comments': comments, 'form': form})

    def post(self, request, pk):
        news_item = get_object_or_404(News, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
        comments = news_item.comments.all()
        return render(request, self.template_name, {'news_item': news_item, 'comments': comments, 'form': form})


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
        year = int(request.GET.get('year', now().year))
        edit_year = int(request.GET.get('edit_year', now().year))
        edit_month = int(request.GET.get('edit_month', now().month))

        entries = FinanceEntry.objects.filter(year=year)
        months_data = {entry.month: entry for entry in entries}
        profits = [months_data.get(i).profit if i in months_data else 0 for i in range(1, 13)]

        income_agg = entries.aggregate(
            match=Sum('match_income'),
            sponsors=Sum('sponsors_income'),
            transfers=Sum('transfers_income'),
            prize=Sum('prize_income'),
            merch=Sum('merch_income'),
            other=Sum('other_income'),
        )
        expense_agg = entries.aggregate(
            transfers=Sum('transfers_expense'),
            salary=Sum('salary_expense'),
            academy=Sum('academy_expense'),
            infra=Sum('infra_expense'),
            merch=Sum('merch_expense'),
        )

        total_income = sum(value or 0 for value in income_agg.values()) if income_agg else 0
        total_expense = sum(value or 0 for value in expense_agg.values()) if expense_agg else 0
        total_profit = total_income - total_expense

        try:
            entry = FinanceEntry.objects.get(year=edit_year, month=edit_month)
            form = FinanceEntryForm(instance=entry)
        except FinanceEntry.DoesNotExist:
            form = FinanceEntryForm(initial={'year': edit_year, 'month': edit_month})

        context = {
            'year': year,
            'profits': profits,
            'months_data': months_data,
            'form': form,
            'edit_year': edit_year,
            'edit_month': edit_month,
            'years': range(now().year - 5, now().year + 2),
            'total_income': total_income,
            'total_expense': total_expense,
            'total_profit': total_profit,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        edit_year = request.POST.get('year')
        edit_month = request.POST.get('month')

        instance = FinanceEntry.objects.filter(year=edit_year, month=edit_month).first()

        form = FinanceEntryForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно сохранена.")
        else:
            messages.error(request, "Ошибка при сохранении записи.")

        return redirect(f"{request.path}?year={edit_year}&edit_year={edit_year}&edit_month={edit_month}")


class FinanceEntryDataView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_director()

    def get(self, request):
        year = request.GET.get('year')
        month = request.GET.get('month')

        entry, created = FinanceEntry.objects.get_or_create(
            year=year,
            month=month,
            defaults={field.name: 0 for field in FinanceEntry._meta.fields if field.name not in ['id', 'year', 'month']}
        )

        data = {
            field.name: getattr(entry, field.name)
            for field in FinanceEntry._meta.fields
            if field.name not in ['id']
        }

        return JsonResponse({'success': True, 'data': data})


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
