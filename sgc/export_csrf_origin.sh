#!/usr/bin/env bash
# Detecta o IP público atual da instância e exporta DJANGO_CSRF_TRUSTED_ORIGINS
# com esse IP, para o Django aceitar formulários POST enviados por
# https://<ip-publico> ou http://<ip-publico> (ver AWS.md, seção "Origin
# checking failed").
#
# O serviço de metadados da AWS (169.254.169.254) costuma estar bloqueado nos
# Learner Labs, então o IP é obtido por um serviço externo de echo de IP.
#
# IMPORTANTE: execute com "source" (ou ". "), não diretamente, para que a
# variável exportada afete o shell atual:
#   source export_csrf_origin.sh
#   python manage.py runserver 0.0.0.0:8000

if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    echo "Este script precisa ser executado com 'source', senão a variável" >&2
    echo "exportada não chega ao seu shell. Use: source ${0}" >&2
    exit 1
fi

PUBLIC_IP=$(curl -s --max-time 5 https://checkip.amazonaws.com | tr -d '[:space:]')

if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(curl -s --max-time 5 https://api.ipify.org | tr -d '[:space:]')
fi

if [ -z "$PUBLIC_IP" ]; then
    echo "Não foi possível detectar o IP público. DJANGO_CSRF_TRUSTED_ORIGINS não foi alterado." >&2
    return 1
fi

export DJANGO_CSRF_TRUSTED_ORIGINS="https://${PUBLIC_IP},http://${PUBLIC_IP}"
echo "DJANGO_CSRF_TRUSTED_ORIGINS definido para: $DJANGO_CSRF_TRUSTED_ORIGINS"
