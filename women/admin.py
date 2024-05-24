from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Women, Category
from django.utils.safestring import mark_safe


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)
        
    
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'slug', 'photo', 'cat', 'husband', 'tags')
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('tags', )
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ('time_create', 'title')
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ('set_published', 'set_draft')
    search_fields = ('title', 'cat__name')
    list_filter = (MarriedFilter, 'cat__name', 'is_published')
    
    @admin.display(description='Краткое описание', ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" width=50>')
        return 'Без фото'
    
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')
    
    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} записей сняты с публикации')
        

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
