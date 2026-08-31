# Sistema de Chamados — Nexa Solutions

API REST para abertura e acompanhamento de chamados de suporte interno, com uma interface HTML simples para consumo da API.

Projeto da disciplina de Manutenção e Evolução de Software.

## Tecnologias

- Python 3.12
- Django 5.x
- Django REST Framework 3.15+
- PostgreSQL 16
- Docker e Docker Compose
- Git

## Estrutura do projeto

```text
nexa-solutions/
├── backend/
│   ├── config/              # settings, urls, wsgi/asgi
│   ├── chamados/            # app principal
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   ├── requirements.txt
│   └── manage.py
├── docker/
│   └── entrypoint.sh        # espera o banco e aplica migrações
├── frontend/
│   └── index.html           # interface simples que consome a API
├── docs/
│   └── issues.md            # demandas da empresa
├── .env.example
├── .gitattributes
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

- Docker e Docker Compose (forma recomendada de execução)
- Python 3.12 ou superior (apenas para execução local)
- Git

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

> ⚠️ **Pendência (INC-05):** as variáveis `POSTGRES_*` já são consumidas pela
> aplicação, mas `DJANGO_SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` ainda usam
> valores fixos no `settings.py`.

## Executar com Docker

Forma recomendada. Com o `.env` criado:

```bash
docker compose up --build
```

O ambiente sobe dois serviços: `db` (PostgreSQL 16) e `api` (Django). O
container da aplicação aguarda o banco ficar disponível e aplica as migrações
automaticamente antes de iniciar o servidor.

A API fica em `http://localhost:8000/api/chamados/`.

Comandos úteis:

```bash
# em segundo plano
docker compose up -d --build

# acompanhar os logs da aplicação
docker compose logs -f api

# parar os containers (os dados do banco são preservados)
docker compose down

# parar e apagar também o volume do banco
docker compose down -v
```

Comandos do Django dentro do container:

```bash
docker compose exec api python manage.py migrate
docker compose exec api python manage.py createsuperuser
docker compose exec api python manage.py test
```

Os dados do PostgreSQL ficam em um volume nomeado (`postgres_data`) e
sobrevivem ao `docker compose down`.

## Executar localmente

Alternativa para desenvolvimento sem Docker. Nesse modo a aplicação usa SQLite,
porque a variável `POSTGRES_HOST` não está definida no ambiente.

```bash
cd backend

python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

A API fica em `http://localhost:8000/api/chamados/`.

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
python manage.py test chamados.tests.CriacaoChamadoTests.test_criacao_sem_titulo_retorna_400
```

No Docker:

```bash
docker compose exec api python manage.py test
```

Os testes usam um banco de dados temporário, criado e destruído
automaticamente. O banco de desenvolvimento não é afetado.

O conjunto está em `backend/chamados/tests.py` e cobre:

| Classe | Cobertura |
| --- | --- |
| `CriacaoChamadoTests` | Criação válida, título obrigatório, status padrão e status inválido |
| `FiltroChamadosPorStatusTests` | Filtro por status, valores inválidos e parâmetro vazio |
| `IndicadoresTests` | Totais por status, cenário vazio e consistência da soma |

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
| `GET` | `/api/indicadores/` | Totais de chamados por status |

### Campos do chamado

| Campo | Tipo | Observação |
| --- | --- | --- |
| `id` | inteiro | Somente leitura |
| `titulo` | texto (até 150) | **Obrigatório**, não pode ficar em branco |
| `descricao` | texto | Detalhamento do problema, opcional |
| `status` | texto | `ABERTO`, `EM_ANDAMENTO` ou `CONCLUIDO` (padrão: `ABERTO`) |
| `criado_em` | data/hora | Somente leitura |
| `atualizado_em` | data/hora | Somente leitura |

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

Uma requisição sem título retorna `400 Bad Request`:

```json
{
  "titulo": ["O título do chamado é obrigatório."]
}
```

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

### Indicadores

Retorna a contagem de chamados agrupada por status.

```bash
curl http://localhost:8000/api/indicadores/
```

Resposta `200 OK`:

```json
{
  "total": 6,
  "abertos": 2,
  "em_andamento": 1,
  "concluidos": 3
}
```

## Interface HTML

O arquivo `frontend/index.html` consome a API em
`http://localhost:8000/api/chamados/`. Com o backend em execução, basta abrir o
arquivo no navegador. Se a porta do backend for alterada, ajuste a constante
`API_URL` dentro do arquivo.

## Estado das demandas

O acompanhamento completo está em [`docs/issues.md`](docs/issues.md).

| Demanda | Classificação | Situação |
| --- | --- | --- |
| INC-01 — Cadastro sem título | Corretiva | Concluída |
| INC-02 — Filtro por status | Evolutiva | Concluída |
| INC-03 — Documentação | Preventiva | Concluída |
| INC-04 — Ambiente Docker | Adaptativa / preventiva | Concluída |
| INC-05 — Configurações sensíveis | Preventiva | Pendente |
| INC-06 — Indicadores | Evolutiva | Concluída |
| INC-07 — Testes automatizados | Preventiva | Concluída |

## Convenções do repositório

- Uma branch por issue, nomeada com o identificador da demanda
  (ex.: `inc-02-filtro-status`).
- Cada branch é integrada por Pull Request, referenciando a issue correspondente.
- Arquivos `.sh` usam quebra de linha LF, garantida pelo `.gitattributes`.