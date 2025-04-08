from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'employment_type', 'experience_level', 'date_posted', 'is_active')
    search_fields = ('title', 'company', 'location')
    list_filter = ('employment_type', 'experience_level', 'is_active')
    ordering = ('-date_posted',)
