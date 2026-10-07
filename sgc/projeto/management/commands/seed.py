from django.core.management.base import BaseCommand
from django.core.management import call_command
from projeto.models import Comentario, Resposta


class Command(BaseCommand):
    help = 'Loads relational fixture and seeds MongoDB with sample comments'

    def handle(self, *args, **kwargs):
        self.stdout.write('Carregando dados relacionais (PostgreSQL/SQLite)...')
        call_command('loaddata', 'initial_data')
        self.stdout.write(self.style.SUCCESS('  Dados relacionais carregados.'))

        self.stdout.write('Populando comentários no MongoDB...')
        Comentario.objects.delete()
        Comentario(projeto=1, autor='Carla', curtidas=3,
                   texto='Projeto muito interessante! Quando começa a próxima etapa?',
                   respostas=[Resposta(autor='Maria Silva', texto='A próxima etapa começa no semestre que vem.'),
                              Resposta(autor='Carla', texto='Obrigada!')]).save()
        Comentario(projeto=1, autor='Pedro', curtidas=1,
                   texto='O sistema vai permitir que alunos se inscrevam nos projetos?').save()
        Comentario(projeto=2, autor='Lucas', curtidas=5,
                   texto='Gostaria de participar como colaborador. Como faço?',
                   respostas=[Resposta(autor='João Souza', texto='Envie um e-mail para a coordenação do projeto.')]).save()
        Comentario(projeto=2, autor='Beatriz',
                   texto='Quais kits de robótica estão sendo utilizados nas oficinas?').save()
        # documento "legado", gravado direto pelo driver só com os campos antigos:
        # o MongoDB aceita sem migration e a aplicação continua lendo normalmente
        Comentario._get_collection().insert_one(
            {'projeto': 3, 'texto': 'Quais sensores estão sendo utilizados no monitoramento?'})
        self.stdout.write(self.style.SUCCESS('  Comentários do MongoDB inseridos.'))

        self.stdout.write(self.style.SUCCESS('Seed completo. Acesse /projeto/ para ver os dados.'))
