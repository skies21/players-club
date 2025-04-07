from django.contrib import admin
from .models import Product, Order, CartItem, Sector, SeatReservation, OrderedItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')

admin.site.register(CartItem)
admin.site.register(Sector)
admin.site.register(SeatReservation)


class OrderedItemInline(admin.TabularInline):
    model = OrderedItem
    readonly_fields = ('product', 'quantity', 'size', 'price')
    extra = 0


class SeatReservationInline(admin.TabularInline):
    model = SeatReservation
    extra = 0
    verbose_name = "Билет"
    verbose_name_plural = "Билеты"
    fields = ('sector', 'row_number', 'seat_number', 'reserved_at')
    readonly_fields = ('sector', 'row_number', 'seat_number', 'reserved_at')
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(order__isnull=False)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_price', 'delivery_method', 'payment_method', 'created_at')
    search_fields = ('user__email', 'full_name', 'email')
    list_filter = ('delivery_method', 'payment_method', 'created_at')
    inlines = [OrderedItemInline, SeatReservationInline]

    readonly_fields = ('total_price', 'created_at')
