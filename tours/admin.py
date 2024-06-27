from django.contrib import admin
from .models import Tour

class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'description', 'available_slots')
    list_filter = ('title', 'price', 'available_slots')
    search_fields = ('title', 'price', 'available_slots')


admin.site.register(Tour, TourAdmin)