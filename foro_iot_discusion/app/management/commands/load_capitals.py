import json
from django.core.management.base import BaseCommand
from app.models import Capital

class Command(BaseCommand):
    help = 'Cargar capitales desde un archivo JSON'

    def handle(self, *args, **kwargs):
        with open('capitales.json', 'r') as file:
            data = json.load(file)
            for item in data:
                Capital.objects.create(pais=item['pais'], capital=item['capital'])
        self.stdout.write(self.style.SUCCESS('Datos de capitales cargados exitosamente'))
