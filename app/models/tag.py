from typing import TYPE_CHECKING, List
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.post import Post

# Tabla intermedia para la relación muchos-a-muchos Post <-> Tag
# No es una clase modelo, es una Table simple
post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    # Relación inversa: un tag aparece en muchos posts
    posts: Mapped[List["Post"]] = relationship(
        "Post", secondary=post_tag, back_populates="tags"
    )
