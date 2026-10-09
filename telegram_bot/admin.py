from django.contrib import admin

from .models import BotLead


@admin.register(BotLead)
class BotLeadAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'grade', 'contact', 'role', 'subject', 'telegram_username', 'processed')
    list_filter = ('processed', 'subject', 'role', 'created_at')
    search_fields = ('name', 'contact', 'telegram_username', 'telegram_name', 'goal')
    list_editable = ('processed',)
    readonly_fields = ('created_at',)
