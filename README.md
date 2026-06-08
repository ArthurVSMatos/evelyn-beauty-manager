# Evelyn Beauty

MVP em Flask para substituir controle em papel de uma profissional de estética. O sistema gerencia clientes, serviços, agendamentos, pagamentos e relatórios em PDF, com interface PWA leve e mobile first.

## Recursos

- Login simples para administrador
- Dashboard com atendimentos do dia, pendências, recebido no mês e remarcações
- CRUD de clientes
- CRUD de tipos de serviços
- CRUD de serviços
- CRUD de agendamentos
- Filtros por data, cliente, serviço, pagamento e status do atendimento
- PDF filtrado por pagos, pendentes, remarcados, cancelados ou todos
- PWA com `manifest.json`, ícone e service worker
- SQLite local para desenvolvimento
- PostgreSQL em produção via `DATABASE_URL`
- Configuração para deploy na Vercel

## Estrutura

```text
app.py
config.py
requirements.txt
vercel.json
models/
controllers/
services/
templates/
static/css/
static/js/
static/icons/
static/manifest.json
static/service-worker.js
```

## Rodando localmente

1. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure variáveis opcionais:

```bash
export SECRET_KEY="uma-chave-segura"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="admin123"
```

4. Execute:

```bash
python app.py
```

5. Acesse:

```text
http://127.0.0.1:5000
```

No primeiro acesso local, o banco SQLite será criado em `instance/evelyn_dev.db`. Também serão criados o usuário admin e os serviços iniciais.

## Login inicial

```text
Usuário: admin
Senha: admin123
```

Em produção, defina `ADMIN_USERNAME` e `ADMIN_PASSWORD` antes do primeiro deploy.

## PostgreSQL

Para usar PostgreSQL local ou em produção:

```bash
export DATABASE_URL="postgresql://usuario:senha@host:5432/banco"
python app.py
```

Também são aceitas URLs no formato `postgres://`, que o app converte para `postgresql://`.

## Deploy na Vercel

1. Crie um projeto na Vercel apontando para este repositório.
2. Configure as variáveis de ambiente:

```text
SECRET_KEY
ADMIN_USERNAME
ADMIN_PASSWORD
DATABASE_URL
```

3. Use um PostgreSQL externo, como Neon, Supabase, Railway ou Render.
4. Faça o deploy. O arquivo `vercel.json` direciona as rotas para `app.py`.

## Relatórios

A tela `Relatórios` usa os mesmos filtros da agenda e gera PDF com ReportLab. Para listar apenas:

- Pagos: escolha `Status do pagamento = Pago`
- Pendentes: escolha `Status do pagamento = Pendente`
- Remarcados: escolha `Status do atendimento = Remarcado`
- Todos: deixe os filtros de status em branco

## Observações de produção

- Troque sempre `SECRET_KEY`.
- Não use a senha padrão em produção.
- Use PostgreSQL para dados reais.
- A autenticação é simples e adequada para MVP administrativo de uma única usuária.
