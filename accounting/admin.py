from django.contrib import admin

from .models import Department, License, Software


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor", "version", "category", "is_critical")
    list_filter = ("category", "is_critical")
    search_fields = ("name", "vendor")


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_number",
        "software",
        "department",
        "status",
        "quantity",
        "expiry_date",
        "responsible",
    )
    list_filter = ("status", "department", "software")
    search_fields = ("inventory_number", "license_key", "responsible")
    autocomplete_fields = ("software", "department")
    readonly_fields = ("created_at", "created_by")
