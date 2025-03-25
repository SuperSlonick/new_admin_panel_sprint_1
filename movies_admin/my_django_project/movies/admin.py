from django.contrib import admin
from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork

# Вложенные формы
class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

# Админка для Filmwork
@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    # Отображаемые колонки
    list_display = ('title', 'type', 'created', 'rating')

    # Фильтры
    list_filter = ('type',)

    # Поля для поиска
    search_fields = ('title', 'description', 'id')

# Админка для жанров
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'description', 'created')

# Админка для персон
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
    list_display = ('full_name', 'created')

