from django.shortcuts import render
from projeto.models import Projeto, contagem_comentarios
from core.models import Professor


def home(request):
    context = {
        'total_projetos': Projeto.objects.count(),
        'total_aprovados': Projeto.objects.filter(aprovado=True).count(),
        'total_professores': Professor.objects.count(),
        'projetos_recentes': Projeto.objects.select_related('coordenador').order_by('-inicio')[:3],
        'mais_comentados': mais_comentados(),
    }
    return render(request, 'home.html', context)


def mais_comentados(n=3):
    # contagem vem do MongoDB (agregação); os dados do projeto vêm do banco relacional
    contagem = sorted(contagem_comentarios().values(), key=lambda d: d['perguntas'], reverse=True)[:n]
    projetos = Projeto.objects.in_bulk([d['_id'] for d in contagem])
    return [dict(d, projeto=projetos[d['_id']]) for d in contagem if d['_id'] in projetos]
