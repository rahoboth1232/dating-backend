from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'age',
        'gender',
        'interested_in',
    )
    search_fields = ('user__username', 'user__email')
    list_filter = ('gender', 'interested_in')


admin.site.register(Profile, ProfileAdmin)
