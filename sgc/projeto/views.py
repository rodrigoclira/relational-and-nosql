from bson import ObjectId, json_util
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db import connection
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import ColaboradorProjeto, Projeto, ProjetoTag, Tipo, TipoProjeto, Comentario, Resposta, contagem_comentarios
from django.conf import settings


def listar(request, tag_name = ""):
    # busca (ORM: Q lookups), filtro por tipo e por tag, combinados com paginação
    busca = request.GET.get('q', '')
    tipo_id = request.GET.get('tipo', '')

    projetos = Projeto.objects.select_related('coordenador').order_by('-inicio')

    if tag_name:
        projetos = projetos.filter(projetotag__tag__tag=tag_name.lower())
    if busca:
        projetos = projetos.filter(titulo__icontains=busca)
    if tipo_id:
        projeto_ids = TipoProjeto.objects.filter(tipo_id=tipo_id).values_list('projeto_id', flat=True)
        projetos = projetos.filter(pk__in=projeto_ids)

    paginator = Paginator(projetos, 5)
    pagina = paginator.get_page(request.GET.get('page'))

    # quantidade de perguntas por projeto vem de UMA agregação no MongoDB
    contagem = contagem_comentarios()
    for projeto in pagina:
        projeto.perguntas = contagem.get(projeto.pk, {}).get('perguntas', 0)

    context = {
        'projetos': pagina,
        'tipos': Tipo.objects.all(),
        'busca': busca,
        'tipo_id': tipo_id,
        'tag_name': tag_name,
    }
    return render(request, 'projeto/list.html', context)

def exibir(request, projeto_id):
    projeto = get_object_or_404(Projeto.objects.select_related('coordenador'), pk=projeto_id)
    colaboradores = ColaboradorProjeto.objects.filter(projeto=projeto).select_related('colaborador')
    tags = ProjetoTag.objects.filter(projeto=projeto).select_related('tag')
    tipos = TipoProjeto.objects.filter(projeto=projeto).select_related('tipo')

    if settings.COMMENTS:
        comentarios = Comentario.objects(projeto = projeto_id)
    else:
        comentarios = []

    context = {
        'projeto': projeto,
        'colaboradores': colaboradores,
        'tags': tags,
        'tipos': tipos,
        'comentarios': comentarios,
        'comentario_settings': settings.COMMENTS
    }

    return render(request, 'projeto/detail.html', context)

def _autor(request):
    if request.user.is_authenticated:
        return request.user.username
    return request.POST.get('autor', '').strip()[:100] or 'anônimo'

def _voltar(projeto_id):
    return redirect(reverse('projeto:exibir', args=[projeto_id]) + '#perguntas')

def _comentario_ou_404(comentario_id):
    if not ObjectId.is_valid(comentario_id):
        raise Http404
    comentario = Comentario.objects(id=comentario_id).only('projeto').first()
    if comentario is None:
        raise Http404
    return comentario

@require_POST
def comentar(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    texto = request.POST.get('texto', '').strip()[:1024]
    if texto:
        Comentario(projeto=projeto.pk, autor=_autor(request), texto=texto).save()
    return _voltar(projeto.pk)

@require_POST
def curtir(request, comentario_id):
    comentario = _comentario_ou_404(comentario_id)
    # $inc: o próprio MongoDB soma 1 de forma atômica (sem ler, somar e salvar)
    Comentario.objects(id=comentario_id).update_one(inc__curtidas=1)
    return _voltar(comentario.projeto)

@require_POST
def responder(request, comentario_id):
    comentario = _comentario_ou_404(comentario_id)
    texto = request.POST.get('texto', '').strip()[:1024]
    if texto:
        # $push: a resposta é inserida DENTRO do documento da pergunta
        Comentario.objects(id=comentario_id).update_one(
            push__respostas=Resposta(autor=_autor(request), texto=texto),
            set__modificado_em=timezone.now(),
        )
    return _voltar(comentario.projeto)

def db_info(request):
    # Trigger queries so connection.queries is populated (requires DEBUG=True)
    projetos = list(Projeto.objects.select_related('coordenador').all())
    sql_queries = connection.queries

    comentarios = list(Comentario.objects.all())
    # documentos "crus", lidos direto pelo driver (pymongo), sem passar pelo mongoengine
    documentos = [json_util.dumps(doc, indent=2, ensure_ascii=False)
                  for doc in Comentario._get_collection().find().sort('projeto')]
    titulos = {p.pk: p.titulo for p in projetos}
    agregacao = [dict(d, projeto=d['_id'], titulo=titulos.get(d['_id'], '?'))
                 for d in sorted(contagem_comentarios().values(), key=lambda d: d['_id'])]

    context = {
        'sql_queries': sql_queries,
        'comentarios': comentarios,
        'documentos': documentos,
        'agregacao': agregacao,
        'projetos': projetos,
    }
    return render(request, 'db_info.html', context)
