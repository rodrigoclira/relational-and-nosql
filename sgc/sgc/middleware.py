from django.conf import settings

#
# Middleware para remover ocorrências repetidas do prefixo FORCE_SCRIPT_NAME no início do path recebido.
# Só é aplicado quando o prefixo FORCE_SCRIPT_NAME está definido no settings (CODE SERVER)
#
class StripDuplicateScriptNameMiddleware:
    """Remove ocorrências repetidas do prefixo FORCE_SCRIPT_NAME no início do
    path recebido.

    Alguns proxies de path (ex.: o proxy "/proxy/<porta>/" do Cloud9/codeweb)
    reescrevem o header Location das respostas de redirect adicionando o
    prefixo de novo, mesmo quando o Django (via FORCE_SCRIPT_NAME) já o
    incluiu — o resultado chega ao navegador com o prefixo duplicado, e na
    requisição seguinte só uma cópia é removida pelo proxy, sobrando outra
    que não bate com nenhuma rota (404). Isso normaliza o path removendo
    qualquer quantidade de cópias repetidas antes do roteamento, sem depender
    de corrigir o proxy (fora do nosso controle).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.prefix = settings.FORCE_SCRIPT_NAME

    def __call__(self, request):
        if self.prefix:
            path = request.path_info
            while path.startswith(self.prefix):
                path = path[len(self.prefix):] or '/'
            if path != request.path_info:
                request.path_info = path
                request.META['PATH_INFO'] = path
        return self.get_response(request)
