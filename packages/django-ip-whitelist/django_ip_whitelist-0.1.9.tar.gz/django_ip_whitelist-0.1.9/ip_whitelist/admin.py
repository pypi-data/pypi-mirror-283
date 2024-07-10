from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext as _
from import_export.admin import ExportMixin
from import_export.resources import ModelResource

from .models import AllowedIP, AllowedIPRange


class AllowedIPResource(ModelResource):
    class Meta:
        model = AllowedIP
        fields = (
            "id",
            "owner",
            "address",
        )


@admin.register(AllowedIP)
class AllowedIPAdmin(ExportMixin, admin.ModelAdmin):
    change_list_template = "ip_whitelist/admin/change_list.html"

    resource_class = AllowedIPResource
    list_display = ("address", "owner")
    search_fields = (
        "owner",
        "address",
    )

    def changelist_view(self, request, extra_context=None):
        my_context = {
            'extra_results': settings.WHITELIST_IPS,
            "extra_results_header": _("Preconfigured IPs")
        }
        return super().changelist_view(request, extra_context=my_context)


class AllowedIPRangeResource(ModelResource):
    class Meta:
        model = AllowedIPRange
        fields = (
            "id",
            "owner",
            "range",
        )


@admin.register(AllowedIPRange)
class AllowedIPRangeAdmin(ExportMixin, admin.ModelAdmin):
    change_list_template = "ip_whitelist/admin/change_list.html"

    resource_class = AllowedIPRangeResource
    list_display = ("range", "owner")
    search_fields = (
        "owner",
        "range",
    )

    def changelist_view(self, request, extra_context=None):
        my_context = {
            'extra_results': settings.WHITELIST_IP_RANGES,
            "extra_results_header": _("Preconfigured IP Ranges")
        }
        return super().changelist_view(request, extra_context=my_context)
