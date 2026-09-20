from datetime import datetime, date

from sqlalchemy import DateTime, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )


class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    total_area: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    area_unit: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    field_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fields.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    farm_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("farms.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    area: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

class Crop(Base):
    __tablename__ = "crops"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    season_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("seasons.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    variety: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    sowing_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    harvest_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )



class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    crop_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False
    )

    activity_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    activity_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )


class Input(Base):
    __tablename__ = "inputs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    crop_id: Mapped[int] = mapped_column(Integer, ForeignKey("crops.id"), nullable=False)

    input_name: Mapped[str] = mapped_column(String, nullable=False)
    input_type: Mapped[str] = mapped_column(String, nullable=False)

    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False)

    application_date: Mapped[date] = mapped_column(Date, nullable=False)

    cost: Mapped[float] = mapped_column(Float, nullable=False)

    description: Mapped[str | None] = mapped_column(String, nullable=True)


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    crop_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False
    )

    expense_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    expense_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )


class Harvest(Base):
    __tablename__ = "harvests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    crop_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False
    )

    harvest_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    unit: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    selling_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )