from django.contrib import admin

from .models import Author, Quote


class QuoteInLine(admin.TabularInline):
    model = Quote


@admin.register(Quote)
class QuoteModelAdmin(admin.ModelAdmin):
    list_display = ["text", 'author']


@admin.register(Author)
class AuthorModelAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [QuoteInLine]
