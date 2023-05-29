import csv
from os import walk

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        models = [Category, Comment, TitleGenre, Genre, Review, Title, User]
        files = [names for names in walk('static/data')][0][2]
        models_files = dict(zip(models, files))

        for model, file in models_files.items():
            with open(f'static/data/{file}', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for column in reader:
                    if column.get('author'):
                        column['author'] = User.objects.get(
                            id=column['author']
                        )
                    _, created = model.objects.get_or_create(
                        **column
                    )
