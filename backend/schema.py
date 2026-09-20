
from datetime import date as DateType

from pydantic import BaseModel, EmailStr


# =========================
# USER
# =========================

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class LoginUser(BaseModel):
    email: EmailStr
    password: str


# =========================
# FARM
# =========================

class CreateFarm(BaseModel):
    name: str
    location: str
    total_area: float
    area_unit: str


class FarmResponse(BaseModel):
    id: int
    user_id: int
    name: str
    location: str
    total_area: float
    area_unit: str


class UpdateFarm(BaseModel):
    name: str | None = None
    location: str | None = None
    total_area: float | None = None
    area_unit: str | None = None


# =========================
# FIELD
# =========================

class CreateField(BaseModel):
    farm_id: int
    name: str
    area: float


class FieldResponse(BaseModel):
    id: int
    farm_id: int
    name: str
    area: float


class UpdateField(BaseModel):
    name: str | None = None
    area: float | None = None


# =========================
# SEASON
# =========================

class CreateSeason(BaseModel):
    field_id: int
    name: str
    start_date: DateType
    end_date: DateType | None = None


class SeasonResponse(BaseModel):
    id: int
    field_id: int
    name: str
    start_date: DateType
    end_date: DateType | None


class UpdateSeason(BaseModel):
    name: str | None = None
    start_date: DateType | None = None
    end_date: DateType | None = None


# =========================
# CROP
# =========================

class CreateCrop(BaseModel):
    season_id: int
    name: str
    variety: str | None = None
    sowing_date: DateType | None = None
    harvest_date: DateType | None = None


class CropResponse(BaseModel):
    id: int
    season_id: int
    name: str
    variety: str | None
    sowing_date: DateType | None
    harvest_date: DateType | None


class UpdateCrop(BaseModel):
    name: str | None = None
    variety: str | None = None
    sowing_date: DateType | None = None
    harvest_date: DateType | None = None


# =========================
# ACTIVITY
# =========================

class CreateActivity(BaseModel):
    crop_id: int
    activity_type: str
    activity_date: DateType
    description: str | None = None


class ActivityResponse(BaseModel):
    id: int
    crop_id: int
    activity_type: str
    activity_date: DateType
    description: str | None


class UpdateActivity(BaseModel):
    activity_type: str | None = None
    activity_date: DateType | None = None
    description: str | None = None


# =========================
# INPUT
# =========================

class CreateInput(BaseModel):
    crop_id: int
    input_name: str
    input_type: str
    quantity: float
    unit: str
    application_date: DateType
    cost: float
    description: str | None = None


class InputResponse(BaseModel):
    id: int
    crop_id: int
    input_name: str
    input_type: str
    quantity: float
    unit: str
    application_date: DateType
    cost: float
    description: str | None


class UpdateInput(BaseModel):
    input_name: str | None = None
    input_type: str | None = None
    quantity: float | None = None
    unit: str | None = None
    application_date: DateType | None = None
    cost: float | None = None
    description: str | None = None


# =========================
# EXPENSE
# =========================

class CreateExpense(BaseModel):
    crop_id: int
    expense_type: str
    amount: float
    expense_date: DateType
    description: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    crop_id: int
    expense_type: str
    amount: float
    expense_date: DateType
    description: str | None


class UpdateExpense(BaseModel):
    expense_type: str | None = None
    amount: float | None = None
    expense_date: DateType | None = None
    description: str | None = None


# =========================
# HARVEST
# =========================

class CreateHarvest(BaseModel):
    crop_id: int
    harvest_date: DateType
    quantity: float
    unit: str
    selling_price: float | None = None
    description: str | None = None


class HarvestResponse(BaseModel):
    id: int
    crop_id: int
    harvest_date: DateType
    quantity: float
    unit: str
    selling_price: float | None
    description: str | None


class UpdateHarvest(BaseModel):
    harvest_date: DateType | None = None
    quantity: float | None = None
    unit: str | None = None
    selling_price: float | None = None
    description: str | None = None


# =========================
# FARM HISTORY
# =========================

class CropHistoryResponse(BaseModel):
    crop: CropResponse
    season: SeasonResponse
    activities: list[ActivityResponse]
    inputs: list[InputResponse]
    expenses: list[ExpenseResponse]
    harvests: list[HarvestResponse]


# =========================
# AI QUERY
# =========================

class QueryRequest(BaseModel):
    question: str


class EvidenceItem(BaseModel):
    type: str
    name: str
    quantity: float | None = None
    unit: str | None = None
    amount: float | None = None
    date: DateType | None = None
    description: str | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    evidence: list[EvidenceItem]


class TimelineItem(BaseModel):
    id: int
    record_type: str
    name: str
    date: DateType
    quantity: float | None = None
    unit: str | None = None
    amount: float | None = None
    description: str | None = None
    crop_name: str | None = None
    field_name: str | None = None
    season_name: str | None = None


class FarmHistoryResponse(BaseModel):
    records: list[TimelineItem]