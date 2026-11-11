# 🤖 Divulgador Inteligente

Robô completo pra divulgar promoções da Shopee automaticamente no **Telegram** e em um **site personalizado**, com geração de copy por **IA**, agendamento de horários e encurtamento de links.

## ✨ Funcionalidades

- ✅ **Bot do Telegram** com comandos administrativos
- ✅ **Postagens automáticas** com foto + texto + link de afiliado
- ✅ **Agendamento** em horários específicos (cron)
- ✅ **Site de promoções** (vitrine responsiva)
- ✅ **Integração com Shopee** (busca ofertas e converte links de afiliado)
- ✅ **Geração de copy com IA** (OpenAI) com variações A/B
- ✅ **Encurtador de links** próprio + integração Bitly
- ✅ **Rastreamento de cliques**
- ✅ **Templates personalizáveis** (Volteou/baixou/urgência/desconto/prova social)

## 📁 Estrutura

```
shopee_smart_bot/
├── main.py                      # Ponto de entrada (site + bot + agendador)
├── app/
│   ├── factory.py               # Cria o FastAPI e controla startup/shutdown
│   ├── models/                  # Entidades: Product, Post, Click
│   ├── repositories/            # Consultas ao banco (ProductRepository, ClickRepository)
│   ├── routes/
│   │   ├── web.py               # Páginas HTML: /, /produto/{id}, /r/{code}
│   │   └── api.py               # JSON: /api/products, /api/stats
│   ├── services/
│   │   ├── shopee/client.py     # Integração API Shopee
│   │   ├── telegram/sender.py   # Envio de postagens aos chats
│   │   ├── telegram/bot.py      # Comandos do bot
│   │   ├── ai/copy_generator.py # Geração de texto com OpenAI
│   │   ├── offers/post_builder.py # Monta a postagem final
│   │   ├── offers/sync.py       # Sincroniza ofertas da Shopee para o banco
│   │   ├── scheduler/jobs.py    # Agendador (APScheduler)
│   │   └── links/shortener.py   # Encurtador de links + cliques
│   ├── templates/               # index.html, product.html
│   └── static/                  # CSS/JS (servido em /static)
├── config/settings.py           # Configurações (.env)
├── database/connection.py       # Engine, sessões e init_db
├── tests/                       # Testes automatizados (pytest)
├── scripts/teste_bot.py         # Teste manual de envio no Telegram
├── requirements.txt             # Dependências
├── requirements-dev.txt         # Dependências de teste
└── .env.example                 # Variáveis a preencher
```

## 🚀 Como rodar (Windows)

### 1. Pré-requisitos
- Python 3.14 (versões das dependências testadas nele)
- Conta de afiliado Shopee (https://affiliate.shopee.com.br)
- Bot criado no Telegram (fale com @BotFather)

### 2. Instalar dependências
```powershell
.\install.bat
```
(cria o `venv`, instala o `requirements.txt` e copia o `.env.example` para `.env`)

### 3. Configurar credenciais
Copie `.env.example` para `.env` e preencha:

```env
# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...   # Token do BotFather
TELEGRAM_CHAT_IDS=-1001234567890        # IDs dos grupos (vírgula)
TELEGRAM_ADMIN_ID=123456789             # Seu ID pessoal

# Shopee Afiliados
SHOPEE_APP_ID=seu_app_id
SHOPEE_SECRET_KEY=sua_secret_key

# OpenAI (opcional, mas recomendado)
OPENAI_API_KEY=sk-...

# Bitly (opcional)
BITLY_TOKEN=seu_token_bitly

# Horários de disparo (formato 24h)
POST_SCHEDULE=09:00,12:00,15:00,18:00,21:00
```

### 4. Rodar
```powershell
.\run.bat
```
ou, na raiz do projeto: `py main.py`

### 5. Testes
```powershell
py -m pip install -r requirements-dev.txt
py -m pytest
```
Os testes usam um banco temporário e não chamam APIs reais.

Teste manual de envio no Telegram: `py scripts/teste_bot.py`

Acesse:
- 🌐 **Site**: http://localhost:8000
- 🤖 **Bot**: converse com seu bot no Telegram
- 📊 **API**: http://localhost:8000/api/products

## 🤖 Comandos do Bot (Telegram)

| Comando | O que faz |
|---------|-----------|
| `/start` | Mostra menu de comandos |
| `/produtos` | Lista produtos com botões pra postar |
| `/postar [id]` | Força postagem de um produto |
| `/novo` | Adiciona novo produto via chat |
| `/agendar` | Mostra próximos horários |
| `/stats` | Estatísticas de cliques |

## 📦 Adicionando produtos

### Via Telegram
```
/novo
Notebook Gamer | 4500.00 | 2999.00 | https://img.url | https://shopee.com.br/produto | Eletrônicos
```

### Via código Python
```python
from app.models import Product
from database import get_session
session = get_session()
p = Product(
    name="Fone Bluetooth",
    original_price=199.90,
    sale_price=99.90,
    image_url="https://...",
    affiliate_url="https://shopee.com.br/...",
    category="Eletrônicos",
)
session.add(p)
session.commit()
```

## 🎨 Templates de copy disponíveis

- `urgencia` - Foco em escassez e tempo limitado
- `beneficios` - Foco em resolver problemas
- `social_proof` - Foco em popularidade
- `desconto` - Foco no % de economia

## 📊 Próximos passos (roadmap)

- [ ] Painel web administrativo (login)
- [ ] Suporte a múltiplas plataformas (Magalu, Amazon, Awin)
- [ ] Analytics avançado (conversão por horário)
- [ ] Geração de vídeos curtos (Reels/TikTok)
- [ ] Teste A/B automático

## ⚠️ Importante

- Respeite os termos da Shopee e do Telegram
- Não exagere nos disparos (risco de spam)
- Use a API oficial de afiliados para rastreamento correto

---

Feito com ❤️ para automatizar suas vendas como afiliado.
