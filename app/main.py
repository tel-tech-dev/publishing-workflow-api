from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Article
from app.schemas import ArticleCreate, ArticleRead, ArticleUpdate


app = FastAPI(
    title="Publishing Workflow API",
    version="0.5.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/articles", response_model=list[ArticleRead])
def get_articles(
    db: Session = Depends(get_db)
):
    statement = select(Article).order_by(Article.id)
    return db.scalars(statement).all()


@app.get("/articles/{article_id}", response_model=ArticleRead)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = db.get(Article, article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    return article


@app.post(
    "/articles",
    response_model=ArticleRead,
    status_code=201
)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db)
):
    db_article = Article(
        title=article.title,
        source_url=(
            str(article.source_url)
            if article.source_url
            else None
        ),
        municipality=article.municipality,
        status=article.status
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article


@app.patch("/articles/{article_id}", response_model=ArticleRead)
def update_article(
    article_id: int,
    update: ArticleUpdate,
    db: Session = Depends(get_db)
):
    article = db.get(Article, article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    update_data = update.model_dump(exclude_unset=True)

    if "source_url" in update_data and update_data["source_url"] is not None:
        update_data["source_url"] = str(update_data["source_url"])

    for field, value in update_data.items():
        setattr(article, field, value)

    db.commit()
    db.refresh(article)

    return article


@app.delete(
    "/articles/{article_id}",
    status_code=204
)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = db.get(Article, article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    db.delete(article)
    db.commit()

    return Response(status_code=204)
