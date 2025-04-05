from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from .forms import MatchForm
from .models import Product, CartItem, Order, Match, Sector, SeatReservation, OrderedItem


class ShopView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'


@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        size = request.POST.get('size', 'M')
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product, size=size)
        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({'message': 'Товар успешно добавлен в корзину!'})
    return JsonResponse({'error': 'Некорректный запрос'}, status=400)


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    seat_reservations = SeatReservation.objects.filter(user=request.user)

    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'seat_reservations': seat_reservations,
        'total_price': total_price,
    })


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        delivery_method = request.POST.get('delivery_method')
        address = request.POST.get('address') if delivery_method == 'delivery' else None
        payment_method = request.POST.get('payment_method')

        cart_items = CartItem.objects.filter(user=request.user)
        seat_reservations = SeatReservation.objects.filter(user=request.user, order__isnull=True)

        if not cart_items and not seat_reservations:
            raise Http404("Корзина пуста")

        products_total = sum(item.total_price() for item in cart_items)
        seats_total = sum(seat.sector.price for seat in seat_reservations)
        total_price = products_total + seats_total

        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            full_name=full_name,
            email=email,
            delivery_method=delivery_method,
            address=address,
            payment_method=payment_method
        )

        for item in cart_items:
            OrderedItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                price=item.product.price  # Фиксируем цену на момент покупки
            )

        # Привязываем забронированные места к заказу
        seat_reservations.update(order=order)
        seat_reservations.delete()

        # Очищаем корзину
        cart_items.delete()

        messages.success(request, 'Заказ успешно создан!')
        return redirect('home')

    return render(request, 'shop/checkout.html')


def match_schedule(request):
    matches = Match.objects.all()
    return render(request, 'shop/match_schedule.html', {'matches': matches})


@login_required
def add_match(request):
    if request.user.role == 'guest':
        return redirect('match_schedule')  # Гость не может добавлять матчи

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Матч успешно добавлен!')
            return redirect('match_schedule')
    else:
        form = MatchForm()

    return render(request, 'shop/add_match.html', {'form': form})


@login_required
def edit_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.user.role == 'guest':
        return redirect('match_schedule')

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            messages.success(request, 'Матч успешно обновлен!')
            return redirect('match_schedule')
    else:
        form = MatchForm(instance=match)

    return render(request, 'shop/edit_match.html', {'form': form})


@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.user.role == 'guest':
        return redirect('match_schedule')

    match.delete()
    messages.success(request, 'Матч успешно удален!')
    return redirect('match_schedule')


@login_required
def remove_seat_from_cart(request, seat_id):
    reservation = get_object_or_404(SeatReservation, id=seat_id, user=request.user)
    reservation.delete()
    messages.success(request, "Место удалено из корзины.")
    return redirect('cart')


def match_sectors(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    sectors = match.sectors.all()
    return render(request, 'shop/match_sectors.html', {'match': match, 'sectors': sectors})


def select_seat(request, sector_id):
    sector = get_object_or_404(Sector, id=sector_id)
    taken_seats = set(sector.reservations.values_list('seat_number', flat=True))
    all_seats = list(range(1, sector.total_seats + 1))
    return render(request, 'shop/select_seat.html', {
        'sector': sector,
        'all_seats': all_seats,
        'taken_seats': taken_seats,
    })


def add_seat_to_cart(request, sector_id):
    if request.method == 'POST':
        seat_number = int(request.POST.get('seat_number'))
        sector = get_object_or_404(Sector, id=sector_id)
        if SeatReservation.objects.filter(sector=sector, seat_number=seat_number).exists():
            messages.error(request, "Место уже занято.")
        else:
            SeatReservation.objects.create(
                sector=sector,
                seat_number=seat_number,
                user=request.user
            )
            messages.success(request, f"Место {seat_number} добавлено в корзину.")

        return redirect('match_sectors', match_id=sector.match.id)
