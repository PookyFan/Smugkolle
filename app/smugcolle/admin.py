# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import *

class UploadedImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(UploadedImage, UploadedImageAdmin)