from django.contrib import admin
from .models import reg,UploadImage
from .models import getintouch

admin.site.register(reg)
admin.site.register(getintouch)
admin.site.register(UploadImage)
