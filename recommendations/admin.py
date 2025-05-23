from django.contrib import admin
from .models import JobLike, Recommendation
from .models import Recommendation


# Register your models here.
@admin.register(JobLike)
class JobLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'timestamp')
    search_fields = ('user__username', 'job__titulo')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
    raw_id_fields = ('user', 'job')

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'score', 'timestamp')
    search_fields = ('user__username', 'job__titulo')
    list_filter = ('timestamp',)
    ordering = ('-score',)
    raw_id_fields = ('user', 'job')