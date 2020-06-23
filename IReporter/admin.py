from django.contrib import admin
from .models import Flag
# Register your models here.
admin.site.register(Flag)

from .models import User,Profile
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
