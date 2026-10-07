"""sgc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static
from django.urls import path, include, re_path
from projeto import views as projeto_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('projeto/', include('projeto.urls')),
    path('db-info/', projeto_views.db_info, name='db_info'),
]

if settings.DEBUG:
    # Rota de apoio para servir os arquivos estáticos quando o projeto roda
    # atrás de um proxy com prefixo de path (ver FORCE_SCRIPT_NAME/STATIC_URL
    # em settings.py): o servidor automático do runserver casa o pedido com
    # STATIC_URL (que já vem com o prefixo), mas a requisição chega ao Django
    # sem o prefixo (removido pelo proxy) — por isso essa rota usa o caminho
    # fixo "static/", sem prefixo, para sempre bater com o que realmente chega.
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve_static),
    ]
