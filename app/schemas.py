from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


ArticleStatus = Literal["draft", "ready", "published"]


class ArticleCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    source_url: HttpUrl | None = None
    municipality: str = Field(min_length=2, max_length=50)
    status: ArticleStatus = "draft"


class ArticleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    source_url: HttpUrl | None = None
    municipality: str | None = Field(default=None, min_length=2, max_length=50)
    status: ArticleStatus | None = None


class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    source_url: str | None
    municipality: str
    status: str
    created_at: datetime
