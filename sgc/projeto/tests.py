from datetime import date

from django.test import TestCase
from django.urls import reverse

from core.models import Professor
from .models import Comentario, Projeto, contagem_comentarios

# Precisa do MongoDB rodando (docker compose up -d). Usa o projeto 9999 para
# não se misturar com os dados do seed e apaga seus documentos ao final.
PK = 9999


class ComentarioMongoTest(TestCase):
    def setUp(self):
        professor = Professor.objects.create(nome='Teste', email='t@t.com', lattes='http://lattes.cnpq.br/1')
        Projeto.objects.create(pk=PK, titulo='Teste', descricao='d', inicio=date(2025, 1, 1),
                               fim=date(2025, 12, 31), coordenador=professor)

    def tearDown(self):
        Comentario.objects(projeto=PK).delete()

    def test_perguntar_curtir_responder(self):
        r = self.client.post(reverse('projeto:comentar', args=[PK]), {'texto': 'Pergunta?', 'autor': 'Ana'})
        self.assertRedirects(r, reverse('projeto:exibir', args=[PK]) + '#perguntas', fetch_redirect_response=False)
        comentario = Comentario.objects.get(projeto=PK)

        self.client.post(reverse('projeto:curtir', args=[comentario.id]))
        self.client.post(reverse('projeto:curtir', args=[comentario.id]))
        self.client.post(reverse('projeto:responder', args=[comentario.id]), {'texto': 'Resposta'})

        comentario.reload()
        self.assertEqual(comentario.autor, 'Ana')
        self.assertEqual(comentario.curtidas, 2)
        self.assertEqual([r.texto for r in comentario.respostas], ['Resposta'])
        self.assertEqual(comentario.respostas[0].autor, 'anônimo')

        c = contagem_comentarios()[PK]
        self.assertEqual((c['perguntas'], c['curtidas'], c['respostas']), (1, 2, 1))

    def test_validacoes(self):
        self.assertEqual(self.client.get(reverse('projeto:comentar', args=[PK])).status_code, 405)
        self.client.post(reverse('projeto:comentar', args=[PK]), {'texto': '   '})
        self.assertEqual(Comentario.objects(projeto=PK).count(), 0)
        self.assertEqual(self.client.post(reverse('projeto:comentar', args=[12345])).status_code, 404)
        self.assertEqual(self.client.post(reverse('projeto:curtir', args=['nao-e-objectid'])).status_code, 404)
        self.assertEqual(self.client.post(reverse('projeto:curtir', args=['0' * 24])).status_code, 404)
