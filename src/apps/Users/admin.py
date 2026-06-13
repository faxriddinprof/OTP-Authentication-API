from django.contrib import admin
from src.apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "tg_id")
    search_fields = ("name", "email", "tg_id")
    list_filter = ("id",)
    readonly_fields = ("id",)
    
    fieldsets = (
        ("Shaxsiy Ma'lumotlar", {
            "fields": ("id", "name", "email")
        }),
        ("Xavfsizlik", {
            "fields": ("password",),
            "classes": ("collapse",)
        }),
        ("Telegram", {
            "fields": ("tg_id",),
            "classes": ("collapse",)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Tahrirlash shaklida
            return self.readonly_fields + ("email",)  
        return self.readonly_fields
