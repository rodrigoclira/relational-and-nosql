# Passos para instalação na AWS com o Cloud9

1. Crie um ambiente com o Cloud9 (use a instância `t3.small`)

2. Abra o terminal do Cloud9 e baixe o projeto do GitHub:

```bash
wget https://github.com/rodrigoclira/relational-and-nosql/archive/refs/heads/main.zip
unzip main.zip
cd relational-and-nosql-main/
```

3. Instale as dependências do projeto:

```bash
pip3 install -r requirements.txt
```

4. Suba o MongoDB via Docker:

```bash
docker compose up -d
```

Para verificar se o MongoDB está rodando:

```bash
docker compose exec mongodb mongosh comments
```

5. Acesse a pasta `sgc` e aplique as migrations:

```bash
cd sgc/
python manage.py migrate
```

6. Popule o banco de dados com os dados de exemplo:

```bash
python manage.py seed
```

Isso carrega os projetos/professores no SQLite e insere comentários de exemplo no MongoDB.

7. Inicie o servidor na porta 8080:

```bash
python manage.py runserver 0.0.0.0:8080
```

8. Clique em `Preview` e escolha `Preview Running Application` e em seguida `Pop out into new Window`.

![image](https://github.com/user-attachments/assets/9e8781a7-918f-4df6-9171-995700fd241c)

![image](https://github.com/user-attachments/assets/0724f536-bb1c-4e45-af27-d00068256dff)

9. Digite agora no navegador:

`https://URL-DO-CLOUD9/projeto`

![image](https://github.com/user-attachments/assets/4379f9a3-50a3-47b0-bb5a-ae484786f62e)


## Banco de dados na AWS

Pesquise e em seguida, altere o projeto para utilizar os serviços de banco de dados gerenciados da AWS.

> Confirmar se todos os serviços estão disponíveis no Learner Lab. 

1. RDS (Banco de Dados Relacional)

2. DocumentDB (MongoDB)

Mais informações sobre os banco de dados da AWS: https://aws.amazon.com/products/databases/

![image](https://github.com/user-attachments/assets/badca81c-ca9b-406b-8037-e97cc63fb693)

## Links e imagens quebrados atrás de proxy com prefixo (ex.: `/proxy/8000/...`) usando o Code Web

Se você estiver acessando a aplicação por um proxy que expõe a porta sob um prefixo (padrão `https://SEU-HOST/proxy/<porta>/...`, comum em ambientes web como Cloud9/codeweb), os links internos gerados pelo Django (`{% url %}`) e os arquivos estáticos (`{% static %}`, como o logo) vêm sem esse prefixo, porque o proxy o remove antes de repassar a requisição — por isso o link/imagem acaba apontando para `https://SEU-HOST/projeto/5` (ou `.../static/core/logo.svg`) em vez de `https://SEU-HOST/proxy/8000/projeto/5`.

Para corrigir, exporte a variável `DJANGO_SCRIPT_NAME` com o mesmo prefixo antes de iniciar o servidor, na mesma porta:

```
export DJANGO_SCRIPT_NAME=/proxy/8000
python manage.py runserver 0.0.0.0:8000
```

Se você mudar de porta, atualize o valor da variável junto (`/proxy/<nova-porta>`). Rodando localmente sem esse proxy, basta não definir a variável (ou `unset DJANGO_SCRIPT_NAME`) para manter o comportamento normal.
