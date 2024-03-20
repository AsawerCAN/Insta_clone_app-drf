from django.contrib import admin
from insta_app.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username')  


admin.site.register(User, UserAdmin)