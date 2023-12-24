from django.contrib import admin
from .models import Deadlines

# Register your models here.

 
@admin.register(Deadlines)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
Deadlines._meta.get_fields()]