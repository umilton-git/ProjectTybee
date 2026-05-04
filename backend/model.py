from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from database import Base

# Image model representing the images table in the database
class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    filepath: Mapped[str] = mapped_column(String(500), unique=True)
    source: Mapped[str] = mapped_column(String(20), index=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

# SessionPreset model representing the session_presets table in the database
class SessionPreset(Base):
    __tablename__ = "session_presets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    image_count: Mapped[int] = mapped_column(Integer)
    duration_seconds: Mapped[int] = mapped_column(Integer)