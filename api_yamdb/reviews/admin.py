from django.contrib import admin

from .models import Category, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "author",
        "score",
    )
    search_fields = ("text",)
    list_filter = (
        "title",
        "text",
    )
    empty_value_display = "пусто"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "пусто"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "пусто"


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "category",
        "description",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "пусто"
