from django.core.management.base import BaseCommand
from django.core.management import call_command
from projeto.models import Comentario


class Command(BaseCommand):
    help = 'Loads relational fixture and seeds MongoDB with sample comments'

    def handle(self, *args, **kwargs):
        self.stdout.write('Carregando dados relacionais (PostgreSQL/SQLite)...')
        call_command('loaddata', 'initial_data')
        self.stdout.write(self.style.SUCCESS('  Dados relacionais carregados.'))

        self.stdout.write('Populando comentários no MongoDB...')
        Comentario.objects.delete()
        Comentario(projeto=1, texto='Projeto muito interessante! Quando começa a próxima etapa?').save()
        Comentario(projeto=1, texto='Quais sensores estão sendo utilizados no monitoramento?').save()
        Comentario(projeto=2, texto='Gostaria de participar como colaborador. Como faço?').save()
        Comentario(projeto=2, texto='XAI é um tema super relevante, parabéns pela iniciativa!').save()
        self.stdout.write(self.style.SUCCESS('  Comentários do MongoDB inseridos.'))

        self.stdout.write(self.style.SUCCESS('Seed completo. Acesse /projeto/ para ver os dados.'))
