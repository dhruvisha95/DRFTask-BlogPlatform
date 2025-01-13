from django.contrib import admin
from .models import Category, Tag, Blog, Comments

# Register your models here.

admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Comments)
