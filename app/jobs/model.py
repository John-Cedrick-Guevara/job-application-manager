from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    company: Mapped[str] = mapped_column(String(200), index=True)
    location: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(String(500))
    source: Mapped[str] = mapped_column(String(200), index=True)
    posted_at: Mapped[Date] = mapped_column(Date, index=True)

