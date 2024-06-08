from django.contrib import admin
from myapp.models import UserModel, NotesModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    readonly_fields = ('answer', )


admin.site.register(NotesModel)
