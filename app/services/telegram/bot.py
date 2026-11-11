"""
Bot do Telegram - comandos administrativos.
Roda em paralelo ao site FastAPI.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.models import Product
from app.repositories import ClickRepository, ProductRepository
from app.services.offers.post_builder import post_builder
from config import settings
from database import session_scope

logger = logging.getLogger(__name__)


# ===========================================
# COMANDOS DO BOT
# ===========================================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - mensagem de boas-vindas"""
    if update.effective_user.id != settings.TELEGRAM_ADMIN_ID:
        return

    msg = (
        "🤖 <b>Divulgador Inteligente</b>\n\n"
        "Comandos disponíveis:\n\n"
        "/produtos - Lista produtos cadastrados\n"
        "/postar [id] - Força postagem de um produto\n"
        "/novo - Adiciona novo produto manualmente\n"
        "/agendar - Mostra próximos horários\n"
        "/stats - Estatísticas de cliques\n"
        "/pausar - Pausa postagens automáticas\n"
        "/retomar - Retoma postagens automáticas"
    )
    await update.message.reply_text(msg, parse_mode="HTML")


async def cmd_produtos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista produtos ativos"""
    if update.effective_user.id != settings.TELEGRAM_ADMIN_ID:
        return

    with session_scope() as session:
        products = ProductRepository(session).list_active()
        if not products:
            await update.message.reply_text("Nenhum produto cadastrado.")
            return

        keyboard = []
        for p in products[:20]:
            label = f"📦 {p.name[:30]}... R$ {p.sale_price:.2f}" if p.sale_price else f"📦 {p.name[:30]}..."
            keyboard.append([InlineKeyboardButton(label, callback_data=f"post_{p.id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"📦 <b>{len(products)} produtos ativos</b>\nClique para postar:",
            reply_markup=reply_markup,
            parse_mode="HTML",
        )


async def callback_post_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback do botão 'Postar' na listagem de produtos"""
    query = update.callback_query
    await query.answer()

    if query.from_user.id != settings.TELEGRAM_ADMIN_ID:
        return

    product_id = int(query.data.split("_")[1])
    with session_scope() as session:
        product = ProductRepository(session).get_by_id(product_id)
        if not product:
            await query.edit_message_text("❌ Produto não encontrado.")
            return

        # Posta o produto
        result = await post_builder.auto_post(product)
        await query.edit_message_text(f"✅ Postado! {result}")


async def cmd_novo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adiciona novo produto manualmente via conversa"""
    if update.effective_user.id != settings.TELEGRAM_ADMIN_ID:
        return

    await update.message.reply_text(
        "📝 Envie os dados do produto neste formato:\n\n"
        "<code>nome | preço original | preço promo | url_imagem | link_afiliado | categoria</code>",
        parse_mode="HTML",
    )
    context.user_data["awaiting_product"] = True


async def handle_product_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe dados do novo produto"""
    if not context.user_data.get("awaiting_product"):
        return

    try:
        parts = [p.strip() for p in update.message.text.split("|")]
        if len(parts) != 6:
            await update.message.reply_text("❌ Formato inválido. Use 6 campos separados por |")
            return

        name, original, sale, image, link, category = parts
        product = Product(
            name=name,
            original_price=float(original),
            sale_price=float(sale),
            image_url=image,
            affiliate_url=link,
            category=category,
            discount=int((1 - float(sale) / float(original)) * 100),
        )
        with session_scope() as session:
            ProductRepository(session).add(product)
            await update.message.reply_text(f"✅ Produto '{name}' cadastrado! ID: {product.id}")

        context.user_data["awaiting_product"] = False
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra estatísticas"""
    if update.effective_user.id != settings.TELEGRAM_ADMIN_ID:
        return

    with session_scope() as session:
        total_clicks = ClickRepository(session).count()
        total_products = ProductRepository(session).count_active()
        await update.message.reply_text(
            f"📊 <b>Estatísticas</b>\n\n"
            f"📦 Produtos ativos: {total_products}\n"
            f"🖱 Cliques rastreados: {total_clicks}",
            parse_mode="HTML",
        )


# ===========================================
# INICIALIZAÇÃO
# ===========================================

def build_application() -> Application:
    """Constrói a aplicação do bot"""
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("produtos", cmd_produtos))
    app.add_handler(CommandHandler("novo", cmd_novo))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CallbackQueryHandler(callback_post_product, pattern=r"^post_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_data))

    return app


async def run_bot_async():
    """Roda o bot em modo async (chamado pelo main)"""
    app = build_application()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info("✅ Bot do Telegram iniciado")
