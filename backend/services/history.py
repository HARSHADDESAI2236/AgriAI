
from fastapi import HTTPException
from sqlalchemy import select

from models import (
    Crop,
    Season,
    Field,
    Farm,
    Activity,
    Input,
    Expense,
    Harvest,
)


async def get_crop_history(
    db,
    crop_id: int,
    user_id: int,
):
    # --------------------------------
    # GET CROP + VERIFY OWNERSHIP
    # --------------------------------
    result = await db.execute(
        select(Crop, Season, Field, Farm)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == crop_id,
            Farm.user_id == user_id,
        )
    )

    row = result.first()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    crop, season, field, farm = row

    history = []

    # --------------------------------
    # ACTIVITIES
    # --------------------------------
    result = await db.execute(
        select(Activity)
        .where(Activity.crop_id == crop_id)
    )

    activities = result.scalars().all()

    for activity in activities:
        history.append({
            "type": "activity",
            "name": activity.activity_type,
            "date": activity.activity_date,
            "description": activity.description,
        })

    # --------------------------------
    # INPUTS
    # --------------------------------
    result = await db.execute(
        select(Input)
        .where(Input.crop_id == crop_id)
    )

    inputs = result.scalars().all()

    for input_record in inputs:
        history.append({
            "type": "input",
            "name": input_record.input_name,
            "quantity": input_record.quantity,
            "unit": input_record.unit,
            "amount": input_record.cost,
            "date": input_record.application_date,
            "description": input_record.description,
        })

    # --------------------------------
    # EXPENSES
    # --------------------------------
    result = await db.execute(
        select(Expense)
        .where(Expense.crop_id == crop_id)
    )

    expenses = result.scalars().all()

    for expense in expenses:
        history.append({
            "type": "expense",
            "name": expense.expense_type,
            "amount": expense.amount,
            "date": expense.expense_date,
            "description": expense.description,
        })

    # --------------------------------
    # HARVESTS
    # --------------------------------
    result = await db.execute(
        select(Harvest)
        .where(Harvest.crop_id == crop_id)
    )

    harvests = result.scalars().all()

    for harvest in harvests:
        history.append({
            "type": "harvest",
            "name": "Harvest",
            "quantity": harvest.quantity,
            "unit": harvest.unit,
            "amount": harvest.selling_price,
            "date": harvest.harvest_date,
            "description": harvest.description,
        })

    # --------------------------------
    # SORT BY DATE
    # --------------------------------
    history.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return {
        "crop": {
            "id": crop.id,
            "name": crop.name,
            "variety": crop.variety,
            "sowing_date": crop.sowing_date,
            "harvest_date": crop.harvest_date,
            "field_name": field.name,
            "season_name": season.name,
            "farm_name": farm.name,
        },
        "history": history,
    }

async def get_farm_history(
    db,
    user_id: int,
    field_id: int | None = None,
    season_id: int | None = None,
    crop_id: int | None = None,
    record_type: str | None = None,
):
    records = []

    # -------------------------
    # ACTIVITIES
    # -------------------------
    if record_type is None or record_type == "activity":

        result = await db.execute(
            select(Activity, Crop, Season, Field)
            .join(Crop, Activity.crop_id == Crop.id)
            .join(Season, Crop.season_id == Season.id)
            .join(Field, Season.field_id == Field.id)
            .join(Farm, Field.farm_id == Farm.id)
            .where(Farm.user_id == user_id)
        )

        rows = result.all()

        for activity, crop, season, field in rows:

            if field_id is not None and field.id != field_id:
                continue

            if season_id is not None and season.id != season_id:
                continue

            if crop_id is not None and crop.id != crop_id:
                continue

            records.append({
                "id": activity.id,
                "record_type": "activity",
                "name": activity.activity_type,
                "date": activity.activity_date,
                "quantity": None,
                "unit": None,
                "amount": None,
                "description": activity.description,
                "crop_name": crop.name,
                "field_name": field.name,
                "season_name": season.name,
            })

    # -------------------------
    # INPUTS
    # -------------------------
    if record_type is None or record_type == "input":

        result = await db.execute(
            select(Input, Crop, Season, Field)
            .join(Crop, Input.crop_id == Crop.id)
            .join(Season, Crop.season_id == Season.id)
            .join(Field, Season.field_id == Field.id)
            .join(Farm, Field.farm_id == Farm.id)
            .where(Farm.user_id == user_id)
        )

        rows = result.all()

        for input_record, crop, season, field in rows:

            if field_id is not None and field.id != field_id:
                continue

            if season_id is not None and season.id != season_id:
                continue

            if crop_id is not None and crop.id != crop_id:
                continue

            records.append({
                "id": input_record.id,
                "record_type": "input",
                "name": input_record.input_name,
                "date": input_record.application_date,
                "quantity": input_record.quantity,
                "unit": input_record.unit,
                "amount": input_record.cost,
                "description": input_record.description,
                "crop_name": crop.name,
                "field_name": field.name,
                "season_name": season.name,
            })

    # -------------------------
    # EXPENSES
    # -------------------------
    if record_type is None or record_type == "expense":

        result = await db.execute(
            select(Expense, Crop, Season, Field)
            .join(Crop, Expense.crop_id == Crop.id)
            .join(Season, Crop.season_id == Season.id)
            .join(Field, Season.field_id == Field.id)
            .join(Farm, Field.farm_id == Farm.id)
            .where(Farm.user_id == user_id)
        )

        rows = result.all()

        for expense, crop, season, field in rows:

            if field_id is not None and field.id != field_id:
                continue

            if season_id is not None and season.id != season_id:
                continue

            if crop_id is not None and crop.id != crop_id:
                continue

            records.append({
                "id": expense.id,
                "record_type": "expense",
                "name": expense.expense_type,
                "date": expense.expense_date,
                "quantity": None,
                "unit": None,
                "amount": expense.amount,
                "description": expense.description,
                "crop_name": crop.name,
                "field_name": field.name,
                "season_name": season.name,
            })

    # -------------------------
    # HARVESTS
    # -------------------------
    if record_type is None or record_type == "harvest":

        result = await db.execute(
            select(Harvest, Crop, Season, Field)
            .join(Crop, Harvest.crop_id == Crop.id)
            .join(Season, Crop.season_id == Season.id)
            .join(Field, Season.field_id == Field.id)
            .join(Farm, Field.farm_id == Farm.id)
            .where(Farm.user_id == user_id)
        )

        rows = result.all()

        for harvest, crop, season, field in rows:

            if field_id is not None and field.id != field_id:
                continue

            if season_id is not None and season.id != season_id:
                continue

            if crop_id is not None and crop.id != crop_id:
                continue

            records.append({
                "id": harvest.id,
                "record_type": "harvest",
                "name": "Harvest",
                "date": harvest.harvest_date,
                "quantity": harvest.quantity,
                "unit": harvest.unit,
                "amount": harvest.selling_price,
                "description": harvest.description,
                "crop_name": crop.name,
                "field_name": field.name,
                "season_name": season.name,
            })

    # Newest first
    records.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return records