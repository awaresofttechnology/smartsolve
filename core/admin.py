import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Contact

admin.site.site_header = "SmartSync Administration"
admin.site.site_title = "SmartSync Admin"
admin.site.index_title = "Welcome to SmartSync Dashboard"


def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="contacts.csv"'
    writer = csv.writer(response)
    writer.writerow(["First Name", "Last Name", "Email", "Service", "Message", "Submitted At"])
    for obj in queryset:
        writer.writerow([obj.fname, obj.lname, obj.email, obj.service, obj.message, obj.submitted_at])
    return response

export_as_csv.short_description = "Export selected to CSV"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "service_badge", "short_message", "submitted_at")
    list_display_links = ("full_name", "email")
    list_filter = ("service", "submitted_at")
    search_fields = ("fname", "lname", "email", "message")
    readonly_fields = ("fname", "lname", "email", "service", "message", "submitted_at")
    ordering = ("-submitted_at",)
    date_hierarchy = "submitted_at"
    list_per_page = 25
    actions = [export_as_csv]

    fieldsets = (
        ("Contact Details", {
            "fields": ("fname", "lname", "email"),
        }),
        ("Enquiry", {
            "fields": ("service", "message"),
        }),
        ("Meta", {
            "fields": ("submitted_at",),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Name", ordering="fname")
    def full_name(self, obj):
        return f"{obj.fname} {obj.lname}"

    @admin.display(description="Service")
    def service_badge(self, obj):
        colors = {
            "web-design": "#1a6fd4",
            "web-development": "#7c3aed",
            "seo-ranking": "#f59e0b",
            "link-building": "#ef4444",
            "traffic-growth": "#06b6d4",
            "software-development": "#10b981",
            "keyword-research": "#f97316",
            "sitemap-optimization": "#8b5cf6",
        }
        color = colors.get(obj.service, "#6b7280")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            color,
            obj.service.replace("-", " ").title(),
        )

    @admin.display(description="Message Preview")
    def short_message(self, obj):
        return obj.message[:80] + "…" if len(obj.message) > 80 else obj.message
