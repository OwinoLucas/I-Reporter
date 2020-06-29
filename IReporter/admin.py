from django.contrib import admin
<<<<<<< HEAD
from .models import Flag
# Register your models here.
admin.site.register(Flag)
from .models import User,Profile
=======
from .models import User,Profile,Flag,InterventionRecord,Tag


>>>>>>> origin/master
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Flag)
admin.site.register(InterventionRecord)
admin.site.register(Tag)