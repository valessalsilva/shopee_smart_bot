"""
Site de promoções - vitrine dos produtos (páginas HTML).
"""
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.repositories import ClickRepository, ProductRepository
from app.services.links import shortener
from database import get_db

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, category: str = None, db: Session = Depends(get_db)):
    """Home: vitrine de promoções"""
    repo = ProductRepository(db)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "products": repo.list_active(category, newest_first=True),
            "categories": repo.list_categories(),
            "current_category": category,
        },
    )


@router.get("/produto/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    """Página de detalhe de um produto"""
    product = ProductRepository(db).get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return templates.TemplateResponse(request, "product.html", {"product": product})


@router.get("/r/{code}")
async def redirect_short(code: str, request: Request, db: Session = Depends(get_db)):
    """Redireciona link encurtado, registrando o clique"""
    click = ClickRepository(db).get_by_code(code, with_product=True)
    if not click:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    # Registra o clique
    shortener.register_click(
        code=code,
        ip=request.client.host,
        user_agent=request.headers.get("user-agent", ""),
    )

    # Redireciona para o link de afiliado
    # Redireciona para o link de afiliado (relacionamento Click.product)
    if click.product:
        return RedirectResponse(url=click.product.affiliate_url)
    return RedirectResponse(url="https://shopee.com.br")
