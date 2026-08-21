"""
Site de promoções - vitrine dos produtos.
FastAPI + Jinja2 (templates HTML).
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from database import Product, Click, get_session, init_db
from services.url_shortener import shortener

app = FastAPI(title="Divulgador Inteligente - Site de Promoções")

# Templates
templates = Jinja2Templates(directory="templates")

# Static (CSS/JS)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup():
    """Inicializa o banco ao subir"""
    init_db()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, category: str = None, db: Session = Depends(get_session)):
    """Home: vitrine de promoções"""
    query = db.query(Product).filter(Product.active == True)
    if category:
        query = query.filter(Product.category == category)
    products = query.order_by(Product.created_at.desc()).all()

    categories = db.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products": products,
            "categories": categories,
            "current_category": category,
        },
    )


@app.get("/produto/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: int, db: Session = Depends(get_session)):
    """Página de detalhe de um produto"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return templates.TemplateResponse(
        "product.html",
        {"request": request, "product": product},
    )


@app.get("/r/{code}")
async def redirect_short(code: str, request: Request, db: Session = Depends(get_session)):
    """Redireciona link encurtado, registrando o clique"""
    click = db.query(Click).filter(Click.short_code == code).first()
    if not click:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    # Registra o clique
    shortener.register_click(
        code=code,
        ip=request.client.host,
        user_agent=request.headers.get("user-agent", ""),
    )

    # Redireciona para o link de afiliado
    product = db.query(Product).filter(Product.id == click.product_id).first()
    if product:
        return RedirectResponse(url=product.affiliate_url)
    return RedirectResponse(url="https://shopee.com.br")


@app.get("/api/products")
async def api_products(category: str = None, db: Session = Depends(get_session)):
    """API JSON com lista de produtos (útil para integrações)"""
    query = db.query(Product).filter(Product.active == True)
    if category:
        query = query.filter(Product.category == category)
    products = query.all()

    return {
        "count": len(products),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "original_price": p.original_price,
                "sale_price": p.sale_price,
                "discount": p.discount,
                "image": p.image_url,
                "link": p.affiliate_url,
                "short_link": p.short_url,
                "category": p.category,
            }
            for p in products
        ],
    }


@app.get("/api/stats")
async def api_stats(db: Session = Depends(get_session)):
    """API com estatísticas"""
    return {
        "total_products": db.query(Product).filter(Product.active == True).count(),
        "total_clicks": db.query(Click).count(),
    }
