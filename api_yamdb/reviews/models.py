from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()
LIMITTEXT = 15


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField("URL жанра", unique=True, max_length=50)

    class Meta:
        verbose_name = "Жанр"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField("URL категории", unique=True, max_length=50)

    class Meta:
        verbose_name = "Категория"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений на сайте."""
    name = models.CharField("Название", max_length=256)
    year = models.IntegerField("Год выхода", validators=(validate_year,))
    description = models.TextField("Описание", blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, related_name="titles", verbose_name="Жанр", through='TitleGenre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="title",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Review(models.Model):
    """Модель обзоров."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
        db_index=True,
        null=False,
    )
    text = models.TextField("Содержание отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
        db_index=True,
        null=False,
    )
    score = models.PositiveSmallIntegerField(
        "Оценка",
        null=False,
        validators=(
            MinValueValidator(
                1,
                "Минимум 1",
            ),
            MaxValueValidator(
                10,
                "Максимум 10",
            ),
        ),
    )
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "title",
                    "author",
                ),
                name="unique_title_author",
            ),
        )

    def __str__(self):
        return self.text[:LIMITTEXT]


class Comment(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
    )
    review = models.ForeignKey(
        Review,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Комментируемый отзыв",
    )
    text = models.TextField("Ваш комментарий")
    pub_date = models.DateTimeField(
        "Дата комментария", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:LIMITTEXT]


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre_pair'
            )
        ]

    def __str__(self):
        return f'{self.title} {self.genre}'
