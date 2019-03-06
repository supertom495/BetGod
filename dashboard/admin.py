from django.contrib import admin
from .models import Event


# Register your models here.
from dashboard.models import Author


class AuthorAdminModel(admin.ModelAdmin):

    list_display = ['user', 'mobile']
    search_fields = ('mobile', 'user__username')

    class Meta:
        model = Author


admin.site.register(Author, AuthorAdminModel)
admin.site.register(Event)