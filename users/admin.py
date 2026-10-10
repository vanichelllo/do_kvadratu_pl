from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from .models import CustomUser, PurchaseHistory


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Стандартна адмінка користувачів Django: пароль хешується при створенні,
    # хеш не показується у формі, є пошук і фільтри
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'role', 'target_grade', 'balance', 'is_staff', 'date_joined')
    list_filter = ('role', 'target_grade', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'username', 'tutor_request__real_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('purchased_materials', 'groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Особисті дані', {'fields': ('first_name', 'last_name', 'phone_number', 'role', 'target_grade',
                                      'telegram_id')}),
        ('Баланс і покупки', {'fields': ('balance', 'purchased_materials')}),
        ('Права доступу', {'classes': ('collapse',),
                           'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Дати', {'fields': ('last_login', 'date_joined')}),
        ('Згода з офертою', {'fields': ('terms_accepted_at', 'terms_version')}),
    )
    readonly_fields = ('terms_accepted_at', 'terms_version')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'usable_password', 'password1', 'password2'),
            'description': "Username можна вказати такий самий, як email.",
        }),
    )


@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    # Архів покупок старим способом (поточні покупки — у «Orders»)
    list_display = ('student', 'material', 'price_paid', 'timestamp')
    search_fields = ('student__email', 'material__title')
    list_filter = ('timestamp',)
