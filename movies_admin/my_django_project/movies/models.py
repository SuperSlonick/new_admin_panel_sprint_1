from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

# Абстрактные миксины
class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

# Жанры
class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name

# Люди (актёры, режиссёры и т.д.)
class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    def __str__(self):
        return self.full_name

# Типы кинопроизведений
class TypeChoices(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV Show')

# Кинопроизведения
class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    type = models.CharField(_('type'), max_length=10, choices=TypeChoices.choices, default=TypeChoices.MOVIE)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork', verbose_name=_('genres'))
    persons = models.ManyToManyField(Person, through='PersonFilmwork', verbose_name=_('persons'))

    class Meta:
        db_table = 'content"."filmwork'
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        return self.title

# Промежуточная таблица "Жанр – Кинопроизведение"
class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('filmwork'))
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('Genre-Filmwork relation')
        verbose_name_plural = _('Genre-Filmwork relations')

# Промежуточная таблица "Человек – Кинопроизведение"
class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('filmwork'))
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('person'))
    role = models.TextField(_('role'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('Person-Filmwork relation')
        verbose_name_plural = _('Person-Filmwork relations')

