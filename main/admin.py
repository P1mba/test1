from django.contrib import admin
from .models import Category, Articles
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Articles)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ['category']
    search_fields = ['title', 'text']