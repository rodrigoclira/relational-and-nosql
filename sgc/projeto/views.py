from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.db import connection
from .models import ColaboradorProjeto, Projeto, ProjetoTag, Tag, Comentario
from django.conf import settings


def listar(request, tag_name = ""):

    if tag_name:
        print(tag_name)
        projetosTags = ProjetoTag.objects.filter(tag__tag = tag_name.lower())
        projetos = [projetoTag.projeto for projetoTag in projetosTags]
    else:
        projetos = Projeto.objects.all()

    context = {'projetos': projetos}
    return render(request, 'projeto/list.html', context)

def exibir(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk = projeto_id)
    coolaboradores = ColaboradorProjeto.objects.filter(projeto=projeto)
    tags = ProjetoTag.objects.filter(projeto=projeto)

    if settings.COMMENTS:
        comentarios = Comentario.objects(projeto = projeto_id)
    else:
        comentarios = []

    context = {
        'projeto': projeto,
        'colaboradores': coolaboradores,
        'tags': tags,
        'comentarios': comentarios,
        'comentario_settings': settings.COMMENTS
    }

    return render(request, 'projeto/detail.html', context)

def comentar(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        texto = request.GET.get('comentario')
        projeto = request.GET.get('projeto')
        comentario = Comentario(projeto=projeto, texto=texto)
        comentario.save()
        return JsonResponse({'texto': texto, 'projeto': projeto, 'status':'ok'}, status=200)

def listar_tag(request, tag_id):
    pass

def db_info(request):
    # Trigger queries so connection.queries is populated (requires DEBUG=True)
    projetos = list(Projeto.objects.select_related('coordenador').all())
    sql_queries = connection.queries

    comentarios = list(Comentario.objects.all())

    context = {
        'sql_queries': sql_queries,
        'comentarios': comentarios,
        'projetos': projetos,
    }
    return render(request, 'db_info.html', context)
