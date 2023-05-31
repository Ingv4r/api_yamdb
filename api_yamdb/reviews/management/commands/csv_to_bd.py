import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()


class Command(BaseCommand):
    help = 'Read csv files in "static/data" folder and write them to database'

    def handle(self, *args, **options):
        try:
            csv_read_create(User, 'users.csv')
            csv_read_create(Category, 'category.csv')
            csv_read_create(Title, 'titles.csv')
            csv_read_create(Genre, 'genre.csv')
            csv_read_create(TitleGenre, 'genre_title.csv')
            csv_read_create(Review, 'review.csv')
            csv_read_create(Comment, 'comments.csv')
        except IntegrityError as error:
            raise CommandError(error)

        self.stdout.write(self.style.SUCCESS('Successfully write to db'))


def csv_read_create(model, file):
    """Read a csv file and create a new entry in database."""
    with open(f'static/data/{file}', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for column in reader:
            if column.get('author', None):
                column['author'] = User.objects.get(
                    id=column['author']
                )
            if column.get('category', None):
                column['category'] = Category.objects.get(
                    id=column['category']
                )
            _, created = model.objects.get_or_create(
                **column
            )
