from copy import deepcopy

from django.contrib import admin

from mezzanine.pages.admin import LinkAdmin as BaseLinkAdmin
from mezzanine.pages.models import Link


from protected_assets.models import Agreement, SignedAgreement


class SignedAgreementAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'agreement', 'ip', )
    list_filter = ('timestamp', 'agreement', )
    date_hierarchy = 'timestamp'


class LinkAdmin(BaseLinkAdmin):
    """Customization of LinkAdmin to allow making links only display to authenticated users."""
    fieldsets = deepcopy(BaseLinkAdmin.fieldsets)
    fieldsets[0][1]["fields"] += ("login_required", )


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('version', 'agreement_pdf', 'created')


admin.site.unregister(Link)
admin.site.register(Link, LinkAdmin)
admin.site.register(SignedAgreement, SignedAgreementAdmin)
admin.site.register(Agreement, AgreementAdmin)
