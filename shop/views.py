from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from .forms import MatchForm
from .models import Product, CartItem, Order, Match


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
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


def checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        delivery_method = request.POST.get('delivery_method')
        address = request.POST.get('address') if delivery_method == 'delivery' else None
        payment_method = request.POST.get('payment_method')

        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items:
            raise Http404("Корзина пуста")

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            full_name=full_name,
            email=email,
            delivery_method=delivery_method,
            address=address,
            payment_method=payment_method
        )

        order.items.set(cart_items)
        order.save()

        cart_items.delete()

        messages.success(request, 'Заказ успешно создан!')

        return redirect('home')
    else:
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
