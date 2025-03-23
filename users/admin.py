from django.contrib import admin

from .models import Position, Player, FullName, Medcine, CustomUser


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('surname', 'firstname', 'patronymic', 'position', 'age', 'cost', 'injury_choice', 'injury_date', 'recovery_date')
    search_fields = ('firstname', 'surname', 'patronymic')
    list_filter = ('position', 'injury_choice')
    ordering = ('surname', 'firstname')

class FullNameAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name__surname', 'full_name__firstname')

class MedcineAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'injury', 'injury_date', 'recovery_date')
    search_fields = ('full_name__surname', 'full_name__firstname', 'injury')
    list_filter = ('injury',)

admin.site.register(Position, PositionAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(FullName, FullNameAdmin)
admin.site.register(Medcine, MedcineAdmin)
admin.site.register(CustomUser)
