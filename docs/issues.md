# Demandas da empresa — Nexa Solutions

A empresa encaminhou as demandas abaixo. A dupla deve criar, organizar e acompanhar essas solicitações no sistema de issues do repositório.

## INC-01 — Cadastro sem título gera erro inadequado

**Relato:** ao cadastrar um chamado sem preencher o título, o sistema apresenta comportamento inadequado ou erro interno.

**Classificação esperada:** Manutenção corretiva.

**Critérios de aceite:**

- O campo `titulo` deve ser obrigatório.
- A API não pode retornar erro HTTP 500 para dados inválidos.
- A API deve retornar código HTTP adequado, como 400 ou 422.
- A resposta deve informar claramente que o título é obrigatório.
- Deve existir teste automatizado para esse caso.

## REALIZADA COM SUCESSO ##

## INC-02 — Filtrar chamados por status

**Relato:** a equipe de suporte precisa consultar apenas chamados abertos, em andamento ou concluídos.

**Classificação esperada:** Manutenção evolutiva.

**Critérios de aceite:**

- A rota `GET /api/chamados/` deve aceitar filtro por status.
- Exemplo: `/api/chamados/?status=ABERTO`.
- O retorno deve conter somente chamados com o status informado.
- Parâmetros inválidos devem ser tratados adequadamente.
- Deve existir teste automatizado para o filtro.

## INC-03 — Documentação insuficiente

**Relato:** novos integrantes não conseguem configurar e executar o sistema sem ajuda do time original.

**Classificação esperada:** Manutenção preventiva.

**Critérios de aceite:**

- README completo e atualizado.
- Orientação para criar `.env` a partir de `.env.example`.
- Comandos de execução com Docker.
- Instruções para executar testes.
- Descrição dos principais endpoints.

## INC-04 — Ambiente Docker reproduzível

**Relato:** o sistema funciona somente no computador em que foi criado. A empresa exige ambiente reproduzível.

**Classificação esperada:** Manutenção adaptativa e preventiva.

**Critérios de aceite:**

- Dockerfile funcional.
- Docker Compose com serviços da aplicação e do banco PostgreSQL.
- Uso de variáveis de ambiente.
- Volume para persistência dos dados.
- O ambiente deve iniciar com `docker compose up --build`.
- O banco deve estar disponível antes do backend tentar acessá-lo.

## INC-05 — Configurações sensíveis expostas

**Relato:** configurações como chave secreta e credenciais de banco de dados estão fixadas no código.

**Classificação esperada:** Manutenção preventiva.

**Critérios de aceite:**

- Chave secreta e credenciais devem ser lidas de variáveis de ambiente.
- `.env` deve permanecer ignorado pelo Git.
- `.env.example` deve possuir apenas valores de exemplo.
- Nenhum segredo real deve estar no repositório.

## INC-06 — Indicadores de chamados

**Relato:** a coordenação precisa visualizar rapidamente o volume de chamados.

**Classificação esperada:** Manutenção evolutiva.

**Critérios de aceite:**

- Criar endpoint `GET /api/indicadores/` ou tela equivalente.
- Informar total de chamados.
- Informar total de chamados abertos.
- Informar total de chamados em andamento.
- Informar total de chamados concluídos.
- Criar teste automatizado para a funcionalidade.

## INC-07 — Testes automatizados ausentes

**Relato:** alterações no sistema causam regressões porque não há testes das funcionalidades críticas.

**Classificação esperada:** Manutenção preventiva.

**Critérios de aceite:**

- Teste de criação válida de chamado.
- Teste de criação sem título.
- Teste de filtro por status.
- Teste de indicadores.
- Instruções de execução dos testes no README.