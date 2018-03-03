# -*- coding: UTF-8 -*-
from django.db import models

class UploadedImage(models.Model):
	file = models.ImageField(max_length=511)
	added_at = models.DateTimeField(auto_now_add=True)
	source = models.CharField(max_length=127)
	
