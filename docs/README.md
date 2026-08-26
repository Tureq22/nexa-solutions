# Sistema de Chamados — Nexa Solutions

API REST para abertura e acompanhamento de chamados de suporte interno, com uma interface HTML simples para consumo da API.

Projeto da disciplina de Manutenção e Evolução de Software.

## Tecnologias

- Python 3.12
- Django 5.x
- Django REST Framework 3.15+
- SQLite (desenvolvimento)
- Docker e Docker Compose
- Git

## Estrutura do projeto

```text
nexa-solutions/
├── backend/
│   ├── config/          # settings, urls, wsgi/asgi
│   ├── chamados/        # app principal (model, views, serializer, testes)
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   └── index.html       # interface simples que consome a API
├── docs/
│   └── issues.md        # demandas da empresa
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

- Python 3.12 ou superior
- Git
- Docker e Docker Compose (para execução containerizada)

## Configuração das variáveis de ambiente

O repositório traz um arquivo `.env.example` com todas as variáveis usadas pelo
projeto. O arquivo `.env` real **nunca** é versionado (está no `.gitignore`).

Crie o seu a partir do exemplo:

```bash
# Linux/macOS
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Depois abra o `.env` e ajuste os valores. Variáveis disponíveis:

| Variável | Descrição | Exemplo |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Chave secreta do Django | `troque-esta-chave-em-producao` |
| `DEBUG` | Modo de depuração | `True` |
| `ALLOWED_HOSTS` | Hosts liberados, separados por vírgula | `localhost,127.0.0.1` |
| `POSTGRES_DB` | Nome do banco | `nexa_chamados` |
| `POSTGRES_USER` | Usuário do banco | `nexa_user` |
| `POSTGRES_PASSWORD` | Senha do banco | `troque-esta-senha` |
| `POSTGRES_HOST` | Host do banco | `db` |
| `POSTGRES_PORT` | Porta do banco | `5432` |

> ⚠️ **Pendência (INC-05):** o `settings.py` ainda usa valores fixos no código e
> não lê essas variáveis. O `.env` já deve ser criado, mas só passará a ter
> efeito após a conclusão do INC-05.

## Executar com Docker

```bash
docker compose up --build
```

Para rodar em segundo plano, parar e ver logs:

```bash
docker compose up -d --build
docker compose logs -f api
docker compose down
```

Comandos do Django dentro do container:

```bash
docker compose exec api python manage.py migrate
docker compose exec api python manage.py createsuperuser
docker compose exec api python manage.py test
```

> ⚠️ **Pendência (INC-04):** o `Dockerfile` ainda não instala as dependências do
> `requirements.txt` e o `docker-compose.yml` não sobe o serviço de banco de
> dados. Até o INC-04 ser concluído, use a execução local descrita abaixo.

## Executar localmente

```bash
cd backend

python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt

python manage.py makemigrations chamados
python manage.py migrate

python manage.py runserver
```

A API fica disponível em `http://localhost:8000/api/chamados/`.

> O passo `makemigrations chamados` é obrigatório no primeiro uso: o app ainda
> não possui migrações versionadas, e sem ele a tabela de chamados não é criada.

Para acessar o painel administrativo, crie um usuário:

```bash
python manage.py createsuperuser
```

E acesse `http://localhost:8000/admin/`.

## Executar os testes

Com o ambiente virtual ativo, a partir da pasta `backend/`:

```bash
# todos os testes do projeto
python manage.py test

# apenas o app de chamados, com saída detalhada
python manage.py test chamados -v 2

# uma classe ou um teste específico
python manage.py test chamados.tests.FiltroChamadosPorStatusTests
```

Os testes usam um banco de dados temporário, criado e destruído
automaticamente. O banco de desenvolvimento não é afetado.

No Docker:

```bash
docker compose exec api python manage.py test
```

## Endpoints

Base: `http://localhost:8000/api/`

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/chamados/` | Lista os chamados, do mais recente para o mais antigo |
| `GET` | `/api/chamados/?status=ABERTO` | Lista apenas os chamados com o status informado |
| `POST` | `/api/chamados/` | Cria um novo chamado |
| `GET` | `/api/chamados/<id>/` | Consulta um chamado específico |
| `PUT` | `/api/chamados/<id>/` | Atualiza todos os campos de um chamado |
| `PATCH` | `/api/chamados/<id>/` | Atualiza parcialmente um chamado |

### Campos do chamado

| Campo | Tipo | Observação |
| --- | --- | --- |
| `id` | inteiro | Somente leitura |
| `titulo` | texto (até 150) | Identificação curta do chamado |
| `descricao` | texto | Detalhamento do problema |
| `status` | texto | `ABERTO`, `EM_ANDAMENTO` ou `CONCLUIDO` (padrão: `ABERTO`) |
| `criado_em` | data/hora | Somente leitura |
| `atualizado_em` | data/hora | Somente leitura |

### Filtro por status

O parâmetro `status` é opcional e aceita os valores `ABERTO`, `EM_ANDAMENTO` e
`CONCLUIDO`. O valor não diferencia maiúsculas de minúsculas. Quando o
parâmetro é omitido ou enviado vazio, todos os chamados são retornados.

```bash
curl "http://localhost:8000/api/chamados/?status=ABERTO"
```

Um status inexistente retorna `400 Bad Request`:

```json
{
  "status": ["Status inválido. Valores aceitos: ABERTO, EM_ANDAMENTO, CONCLUIDO."]
}
```

### Criar um chamado

```bash
curl -X POST http://localhost:8000/api/chamados/ \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Impressora sem tinta", "descricao": "Setor financeiro", "status": "ABERTO"}'
```

Resposta `201 Created`:

```json
{
  "id": 1,
  "titulo": "Impressora sem tinta",
  "descricao": "Setor financeiro",
  "status": "ABERTO",
  "criado_em": "2026-08-25T10:00:00-03:00",
  "atualizado_em": "2026-08-25T10:00:00-03:00"
}
```

## Interface HTML

O arquivo `frontend/index.html` consome a API em
`http://localhost:8000/api/chamados/`. Com o backend em execução, basta abrir o
arquivo no navegador. Se a porta do backend for alterada, ajuste a constante
`API_URL` dentro do arquivo.

## Estado das demandas

O acompanhamento completo está em [`docs/issues.md`](docs/issues.md).

| Demanda | Situação |
| --- | --- |
| INC-01 — Cadastro sem título | Pendente |
| INC-02 — Filtro por status | Concluída |
| INC-03 — Documentação | Concluída |
| INC-04 — Ambiente Docker | Pendente |
| INC-05 — Configurações sensíveis | Pendente |
| INC-06 — Indicadores | Pendente |
| INC-07 — Testes automatizados | Parcial (filtro por status coberto) |