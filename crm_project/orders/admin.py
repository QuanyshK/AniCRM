from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(Message)
admin.site.register(Status)
admin.site.register(Category)