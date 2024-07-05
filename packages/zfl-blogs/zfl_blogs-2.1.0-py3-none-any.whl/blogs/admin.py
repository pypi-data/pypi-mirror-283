from django.contrib import admin  # type: ignore
from django.db import models  # type: ignore
from markdownx.widgets import AdminMarkdownxWidget  # type: ignore

from .models import Blog, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")


class BlogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
# admin.site.register(Popular)
