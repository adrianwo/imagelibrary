from django.contrib import admin
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

User = get_user_model()


# Register your models here.
class ProfileInLine(admin.StackedInline):
    model = Profile

    max_num = 1
    extra = 0
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [ProfileInLine]

    def get_inline_instances(self, request, obj=None):
        return obj and super(UserAdmin, self).get_inline_instances(request, obj) or []

    class Media:
        js = ("accounts/js/profile.js",)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
