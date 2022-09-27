from authemail.admin import EmailUserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model


class UserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "is_verified")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Custom Info", {"fields": ("profile_avatar", "followers")}),
    )


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
