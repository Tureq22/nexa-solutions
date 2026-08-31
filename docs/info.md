# Sistema de Chamados — Nexa Solutions

Projeto inicial para a disciplina de Manutenção e Evolução de Software.

## Contexto

A Nexa Solutions possui um sistema interno para abertura e acompanhamento de chamados de suporte.

O projeto possui uma API REST desenvolvida em Django e uma interface HTML simples para consulta e cadastro de chamados.

## Tecnologias

- Python
- Django
- Django REST Framework
- SQLite
- Docker
- Docker Compose
- Git

## Estrutura

```text
backend/   # API Django
frontend/  # Interface HTML simples
docs/      # Documentação e demandas
```

## Executar localmente

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A API estará disponível em:

```text
http://localhost:8000/api/chamados/
```

## Observação

A documentação deste projeto está incompleta. A dupla deverá melhorar este arquivo como parte da atividade.