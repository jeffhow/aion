from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('reservations')

for model_name, model in app.models.items():
    admin.site.register(model) # Register all models
    
# Register your models here.
# from .models import School, Profile

# admin.site.register(School)
# admin.site.register(Profile)