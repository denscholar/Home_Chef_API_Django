from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "email_address",
        "created_at",
    )
    list_filter = (
        "created_at",
        "phone_number",
    )
    list_display_links = ("phone_number",)
