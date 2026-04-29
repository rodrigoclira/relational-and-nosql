from django.contrib import admin
from .models import Projeto, ColaboradorProjeto, Tipo, TipoProjeto, Tag, ProjetoTag


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'coordenador', 'inicio', 'fim', 'aprovado')
    list_filter = ('aprovado',)
    search_fields = ('titulo', 'descricao')


@admin.register(ColaboradorProjeto)
class ColaboradorProjetoAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'colaborador')
    search_fields = ('projeto__titulo', 'colaborador__nome')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    search_fields = ('tag',)


@admin.register(ProjetoTag)
class ProjetoTagAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'tag')


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(TipoProjeto)
class TipoProjetoAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'tipo')
