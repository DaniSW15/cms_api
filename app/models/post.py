from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # NUEVO: Foreign Key a categoría
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones existentes
    author: Mapped["User"] = relationship("User", back_populates="posts")

    # NUEVO: Relación con categoría
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="posts"
    )

    # NUEVO: Relación muchos-a-muchos con tags
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary="post_tag",  # nombre de la tabla intermedia como string
        back_populates="posts",
    )
