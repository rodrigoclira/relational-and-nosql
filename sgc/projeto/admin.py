from django.contrib import admin
from .models import ColaboradorProjeto, Projeto, Tag, Tipo, TipoProjeto, ProjetoTag


class TipoProjetoInline(admin.TabularInline):
    model = TipoProjeto
    extra = 1


class ColaboradorProjetoInline(admin.TabularInline):
    model = ColaboradorProjeto
    extra = 1


class ProjetoTagInline(admin.TabularInline):
    model = ProjetoTag
    extra = 1


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "coordenador", "inicio", "fim", "aprovado"]
    list_filter = ["aprovado", "inicio"]
    search_fields = ["titulo", "descricao", "coordenador__nome"]
    date_hierarchy = "inicio"
    inlines = [TipoProjetoInline, ColaboradorProjetoInline, ProjetoTagInline]


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ["nome"]
    search_fields = ["nome"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]
    search_fields = ["tag"]


admin.site.register(ColaboradorProjeto)
admin.site.register(TipoProjeto)
admin.site.register(ProjetoTag)
