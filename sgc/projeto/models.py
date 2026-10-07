from django.conf import settings
from django.db import models
from django.utils import timezone
from core.models import Professor
import mongoengine


# ---------------------------------------------------------------------------
# MongoDB (mongoengine): perguntas de um projeto.
# Uma pergunta e suas respostas formam UM documento só (respostas embutidas),
# então a página de detalhe lê a conversa inteira com uma única consulta, sem JOIN.
# ---------------------------------------------------------------------------
class Resposta(mongoengine.EmbeddedDocument):
    autor = mongoengine.StringField(max_length=100, default='anônimo')
    texto = mongoengine.StringField(max_length=1024, required=True)
    criado_em = mongoengine.DateTimeField(default=timezone.now)


class Comentario(mongoengine.Document):
    projeto = mongoengine.IntField(required=True)  # referência ao Projeto (pk do banco relacional)
    autor = mongoengine.StringField(max_length=100, default='anônimo')
    texto = mongoengine.StringField(max_length=1024, required=True)
    criado_em = mongoengine.DateTimeField(help_text='criado em')
    modificado_em = mongoengine.DateTimeField(help_text='modificado em', default=timezone.now)
    curtidas = mongoengine.IntField(default=0)
    respostas = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Resposta))

    meta = {'indexes': ['projeto'], 'ordering': ['-criado_em']}

    def save(self, *args, **kwargs):
        if not self.criado_em:
            self.criado_em = timezone.now()
        self.modificado_em = timezone.now()
        return super().save(*args, **kwargs)


def contagem_comentarios():
    """Agregação ($group): perguntas, curtidas e respostas por projeto.
    Equivale a um SELECT projeto, COUNT(*), SUM(curtidas) ... GROUP BY projeto."""
    if not settings.COMMENTS:
        return {}
    pipeline = [
        {'$group': {
            '_id': '$projeto',
            'perguntas': {'$sum': 1},
            'curtidas': {'$sum': {'$ifNull': ['$curtidas', 0]}},
            'respostas': {'$sum': {'$size': {'$ifNull': ['$respostas', []]}}},
        }},
    ]
    return {d['_id']: d for d in Comentario.objects.aggregate(pipeline)}


# Create your models here.
class Tipo(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome}"

class Projeto(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=500, verbose_name="descrição")
    inicio = models.DateField(verbose_name="início")
    fim = models.DateField(blank=True)
    aprovado = models.BooleanField(default=False, verbose_name="Está institucionalizado?")
    coordenador = models.ForeignKey(Professor, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.titulo}"

class TipoProjeto(models.Model):
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.projeto} ({self.tipo})"

class ColaboradorProjeto(models.Model):
    colaborador = models.ForeignKey(Professor, on_delete=models.PROTECT)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.projeto} | {self.colaborador}"

class Tag(models.Model):
    tag = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.tag}"

class ProjetoTag(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.projeto} | {self.tag}"
