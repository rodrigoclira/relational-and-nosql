# ORM e o NoSQL (MongoDB)

Este projeto tem como objetivo destacar a utilização do ORM do django e do NoSQL. 
<br>
Neste projeto o MongoDB é utilizado para persistir as informaçẽos dos comentários dos projetos.


## Pré-requisitos

> 1. **Instalar bibliotecas** informadas no arquivo 'requirements.txt' 

```bash
pip3 install -r requirements.txt
```

> 2. **MongoDB**
>
> Escolha uma das opções abaixo para rodar o MongoDB.

### Opção A — Docker (recomendado)

Suba o container com:

```bash
docker compose up -d
```

Para se conectar ao shell do MongoDB:

```bash
docker compose exec mongodb mongosh comments
```

Para parar:

```bash
docker compose down
```

### Opção B — Instalação local

Use o tutorial do site do MongoDB compatível com o seu SO.
Link direto para o [Amazon Linux](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-amazon/).
Após a instalação, inicie o daemon:

```bash
sudo systemctl start mongod
```

Para se conectar ao shell do MongoDB:

```bash
mongosh comments
```

## Comandos

Execute os comandos abaixo dentro da pasta `sgc/` (onde está o `manage.py`).

### 1. Aplicar as migrations

```bash
python manage.py migrate
```

### 2. Popular o banco de dados

O comando `seed` carrega os dados de exemplo no banco relacional (SQLite/PostgreSQL) **e** insere comentários de exemplo no MongoDB:

```bash
python manage.py seed
```

O que é inserido:
- 3 professores
- 3 tipos de projeto (Pesquisa, Extensão, Ensino) e 4 tags
- 6 projetos com coordenadores, colaboradores, tipos e tags
- 4 comentários no MongoDB (nos projetos 1, 2 e 3)

> O MongoDB precisa estar rodando antes de executar este comando.

### 3. Iniciar a aplicação

```bash
python manage.py runserver
```

Acesse no navegador:

- Início: http://127.0.0.1:8000/
- Projetos: http://127.0.0.1:8000/projeto/
- Admin: http://127.0.0.1:8000/admin/
- Info dos bancos: http://127.0.0.1:8000/db-info/

Na listagem é possível buscar projetos pelo título, filtrar por tipo (Pesquisa, Extensão, Ensino) ou por tag (`/projeto/tag/python`), com resultados paginados — bons exemplos de `QuerySet`, `Paginator` e requisições `GET` do Django. Os dados do projeto vêm do banco relacional; as perguntas na página de detalhe são documentos do MongoDB.

As perguntas mostram quatro vantagens do MongoDB, cada uma comparada com o SQL em `/db-info/` e no [MONGOSH.md](MONGOSH.md):
- **Documento embutido**: as respostas ficam dentro da pergunta (`$push`), lidas numa única consulta, sem JOIN.
- **Atualização atômica**: o botão "Curtir" usa `$inc`, sem ler-somar-gravar.
- **Agregação**: o `$group` conta perguntas por projeto (badges da listagem e "Mais comentados" na página inicial).
- **Schema flexível**: o `seed` grava um documento "legado" sem `autor`/`respostas`, e a aplicação continua funcionando sem migration.

### 4. Acesso ao painel de administrador

Crie um usuário administrador (a criação pede um nome de usuário, e-mail e senha interativamente):

```bash
python manage.py createsuperuser
```

Em seguida, acesse `http://127.0.0.1:8000/admin/` e entre com as credenciais criadas. No admin dá para ver na prática `list_display`, `list_filter`, `search_fields` e inlines (`Tipo`, `Colaborador` e `Tag` editáveis direto na tela do `Projeto`).


## AWS

- [Passo a passo com o Cloud9](AWS.md)

Replique o projeto utilizando uma instância do RDS e do DocumentDB na AWS.

![image](https://github.com/user-attachments/assets/1a043263-ee4d-4ab4-a811-c25823510096)

Se estiver acessando por um proxy que expõe a porta sob um prefixo (ex.: `https://SEU-HOST/proxy/8000/...`, comum em ambientes web como Cloud9/codeweb), os links internos e as imagens/arquivos estáticos do Django podem sair sem esse prefixo e quebrar. Veja como corrigir com a variável `DJANGO_SCRIPT_NAME` na seção ["Links e imagens quebrados atrás de proxy com prefixo" do AWS.md](AWS.md#links-e-imagens-quebrados-atrás-de-proxy-com-prefixo-ex-proxy8000-usando-o-code-web).

## FAQ

### Erros Mongodb
Mongo não inicia, erro com status 14 < https://stackoverflow.com/questions/64608581/mongodb-code-exited-status-14-failed-but-not-any-clear-errors > 

![image](https://user-images.githubusercontent.com/276077/140451154-46459ade-85d0-4839-b24a-dca3c28df0d3.png)

Comandos necessários

```
sudo chown -R mongod:mongod /var/lib/mongo/
sudo chown mongod:mongod /tmp/mongodb-27017.sock

sudo systemctl daemon-reload
```
## Atividade

Usando uma ORM com a framework escolhida, crie os models para representar o mini-mundo apresentado na imagem abaixo: 

![mini-mundo](https://user-images.githubusercontent.com/276077/163811963-bc1325ed-5321-42ce-bc24-b04426f3279b.png)

Considere as seguintes informações: 
- Atributos iniciadas com _dt-_ representam tipos de data. 
- O atributo com o nome _cod_ é do tipo numérico. 
- E-mail é um _varchar_ com validação (quando existente na ORM). 
- Todos os outros tipos são do tipo _varchar_. 

## Referências 
[SQL vs NoSQL, qual usar?
](https://www.treinaweb.com.br/blog/sql-vs-nosql-qual-usar#:~:text=O%20NoSQL%20%C3%A9%20mais%20indicado,flex%C3%ADvel%20no%20suporte%20de%20dados.)

[SQL ou NoSQL: eis a questão!!
](https://imasters.com.br/banco-de-dados/sql-ou-nosql-eis-a-questao)

[Como escolher entre SQL e NoSQL](https://pt.stackoverflow.com/questions/122452/como-escolher-entre-nosql-e-sql)

[Banco de Dados NoSQL: Um manual prático e didático](https://blog.geekhunter.com.br/banco-de-dados-nosql-um-manual-pratico-e-didatico/)
