from datetime import date

from sqlalchemy import String, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    requested_by: Mapped[str] = mapped_column(String(100))
    provider: Mapped[str] = mapped_column(String(50))
    resource_type: Mapped[str] = mapped_column(String(100))
    configuration: Mapped[dict] = mapped_column(JSON)
    location: Mapped[str] = mapped_column(String(100))
    project_id: Mapped[str] = mapped_column(String(100))
    end_date: Mapped[date] = mapped_column(Date)