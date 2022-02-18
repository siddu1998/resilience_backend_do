from django.contrib import admin

from .models import *

from django.forms import TextInput, Textarea
from django.db import models

class PuzzleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':16, 'cols':40})}
    }



# Register your models here.
admin.site.register(Teams)
admin.site.register(Puzzle,PuzzleAdmin)
admin.site.register(PuzzleQueue)
admin.site.register(Players)
admin.site.register(image_mapper)
