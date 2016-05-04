from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from alertas.models import UserOrgan

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class OrgaoInline(admin.StackedInline):
    model = UserOrgan
    can_delete = False
    verbose_name_plural = 'usuarios'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (OrgaoInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from .models import Organ, PhaseType, AlertType, AlertStatus, AlertColor, Alert, AlertIcon, ReportedAlert, Announcement

class OrganAdmin(admin.ModelAdmin):
    list_display = ('id','nome_orgao','responsavel')

class PhaseTypesAdmin(admin.ModelAdmin):
    list_display = ('id','phase_type')

class AlertTypeAdmin(admin.ModelAdmin):
    list_display = ('description','phase_type','alert_color', 'alert_icon', 'id')

class AlertStatusAdmin(admin.ModelAdmin):
    list_display = ('status_code','status_desc')

class AlertColorsAdmin(admin.ModelAdmin):
    list_display = ('color_name','stroke_color','fill_color')

class AlertAdmin(admin.ModelAdmin):
    list_display = ('title','creation_date','active')

class AlertIconAdmin(admin.ModelAdmin):
    list_display = ('icon_name','icon_url','id')


class ReportedAlertAdmin(admin.ModelAdmin):
    list_display = ('title','creation_date','alert_organ','visitor_name','visitor_phone','visitor_email','status')

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'url', 'status', 'announcement_organ')

admin.site.register(Organ, OrganAdmin)
admin.site.register(PhaseType, PhaseTypesAdmin)
admin.site.register(AlertType, AlertTypeAdmin)
admin.site.register(AlertStatus, AlertStatusAdmin)
admin.site.register(AlertColor, AlertColorsAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.register(AlertIcon, AlertIconAdmin)
admin.site.register(ReportedAlert, ReportedAlertAdmin)
admin.site.register(Announcement, AnnouncementAdmin)