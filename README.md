# Super Market

Projeto e‑commerce desenvolvido em Django. Este repositório contém a aplicação "Super Market" — uma loja online com gestão de produtos, carrinho, pagamentos e integrações externas (ex.: ViaCEP).

## Visão Geral

- Nome: Super Market
- Tipo: Aplicação e‑commerce (Django)
- Principais apps: `accounts`, `product`, `cart`, `payment`, `supermarket`

## Funcionalidades

- Autenticação e perfis de usuário
- Catálogo de produtos com imagens
- Carrinho de compras e checkout
- Integração com via CEP (integrações/viacep.py)
- Webhooks e integração de pagamentos (veja `payment/`)
- Painel administrativo do Django

## Tecnologias

- Python 3.10+
- Django
- Banco de dados: PostgreSQL (recomendado) ou SQLite
- Docker & docker-compose
- Nginx (configuração em `nginx/default.conf`)

## Pré-requisitos

- Python 3.10+ e `pip`
- (Opcional) Docker e `docker-compose`
- Variáveis de ambiente para segredos e configurações

## Instalação local (sem Docker)

1. Crie e ative um virtualenv:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Ou cmd
.venv\Scripts\activate.bat
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Configure variáveis de ambiente (exemplo):

- `DJANGO_SECRET_KEY`
- `DATABASE_URL` (ex.: `postgres://user:pass@host:port/dbname`)
- `DEBUG` (True/False)

4. Rode migrações e crie superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

## Usando Docker

1. Build e subir containers:

```bash
docker-compose build
docker-compose up -d
```

2. Ver logs:

```bash
docker-compose logs -f
```

3. Parar e remover containers:

```bash
docker-compose down
```

## Variáveis de ambiente recomendadas

- `DJANGO_SECRET_KEY` — chave secreta do Django
- `DATABASE_URL` — URL do banco
- `DEBUG` — `True` ou `False`
- Credenciais e chaves para provedores de pagamento (conforme `payment/`)

## Migrações & Media

- Migrações: cada app contém sua pasta `migrations/`.
- `media/` contém imagens de produtos e banners — configure `MEDIA_ROOT`/`MEDIA_URL` em `project/settings.py`.

## Testes

Se existirem testes implementados, rode:

```bash
python manage.py test
```

## Estrutura principal

- `accounts/`, `product/`, `cart/`, `payment/`, `supermarket/` — apps principais
- `project/settings.py` — configurações do Django
- `requirements.txt` — dependências Python
- `nginx/default.conf` — configuração nginx para deploy
