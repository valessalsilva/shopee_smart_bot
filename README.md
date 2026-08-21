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
divulgador-inteligente/
├── main.py                      # Inicializa tudo (bot + site + scheduler)
├── app.py                       # Site FastAPI
├── config.py                    # Configurações (.env)
├── database.py                  # Modelos do banco (SQLite)
├── requirements.txt             # Dependências
├── .env.example                 # Variáveis a preencher
├── services/
│   ├── shopee.py                # Integração API Shopee
│   ├── ai_copy.py               # Geração de texto com OpenAI
│   ├── telegram_bot.py          # Bot do Telegram
│   ├── post_builder.py          # Constrói a postagem final
│   ├── url_shortener.py         # Encurtador de links
│   └── scheduler.py             # Agendador (APScheduler)
└── templates/
    ├── index.html               # Vitrine de produtos
    └── product.html             # Detalhe do produto
```

## 🚀 Como rodar (Windows)

### 1. Pré-requisitos
- Python 3.10+ instalado
- Conta de afiliado Shopee (https://affiliate.shopee.com.br)
- Bot criado no Telegram (fale com @BotFather)

### 2. Instalar dependências
```powershell
cd C:\Users\valessa.lopes\divulgador-inteligente
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

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
python main.py
```

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
from database import Product, get_session
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
