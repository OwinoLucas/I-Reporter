from django.contrib import admin
<<<<<<< HEAD
from .models import User,Profile,Flag


=======
from .models import Flag
# Register your models here.
admin.site.register(Flag)

from .models import User,Profile
>>>>>>> 0a9f0e502cf05031bd680e5a00db586b88677c9c
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Flag)