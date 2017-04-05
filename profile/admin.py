from django.contrib import admin

# Register your models here.
from profile.models import Profile, Point, Discount


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'vip_code', 'fullname')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Point)
admin.site.register(Discount)