from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    Crop,
    Season,
    Field,
    Farm,
    Input,
    Activity,
    Harvest,
    Expense
)


# ---------------------------------------------------------
# FIND USER'S CROPS
# ---------------------------------------------------------

async def get_user_crops(
    db: AsyncSession,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(Farm.user_id == user_id)
    )

    return result.scalars().all()


# ---------------------------------------------------------
# FIND RELEVANT CROPS
# ---------------------------------------------------------

def select_crops(crops, question: str):
    question_lower = question.lower()

    mentioned_crops = []

    for crop in crops:
        if crop.name.lower() in question_lower:
            mentioned_crops.append(crop)

    return mentioned_crops if mentioned_crops else crops


# ---------------------------------------------------------
# GET RELEVANT EVIDENCE
# ---------------------------------------------------------

async def get_farm_evidence(
    db: AsyncSession,
    user_id: int,
    question: str
):
    question_lower = question.lower()

    crops = await get_user_crops(db, user_id)

    if not crops:
        return []

    selected_crops = select_crops(crops, question)

    evidence = []

    # -----------------------------------------------------
    # DETECT INTENTS
    # -----------------------------------------------------

    fertilizer_intent = any(word in question_lower for word in [
        "fertilizer",
        "fertiliser",
        "urea",
        "dap",
        "input"
    ])

    expense_intent = any(word in question_lower for word in [
        "spend",
        "spent",
        "expense",
        "expenses",
        "cost",
        "costs"
    ])

    harvest_intent = any(word in question_lower for word in [
        "harvest",
        "harvested",
        "yield",
        "produce",
        "production"
    ])

    revenue_intent = any(word in question_lower for word in [
        "earn",
        "earned",
        "earning",
        "revenue",
        "income",
        "sold",
        "selling",
        "money from"
    ])

    activity_intent = any(word in question_lower for word in [
        "activity",
        "activities",
        "work",
        "worked",
        "performed"
    ])

    # -----------------------------------------------------
    # IF QUESTION DOES NOT MATCH ANY INTENT
    # -----------------------------------------------------

    if not any([
        fertilizer_intent,
        expense_intent,
        harvest_intent,
        revenue_intent,
        activity_intent
    ]):
        return []

    # -----------------------------------------------------
    # FERTILIZER / INPUTS
    # -----------------------------------------------------

    if fertilizer_intent:

        for crop in selected_crops:

            result = await db.execute(
                select(Input)
                .where(Input.crop_id == crop.id)
                .order_by(Input.application_date)
            )

            inputs = result.scalars().all()

            for item in inputs:

                # If a specific input name is mentioned,
                # only return that input.
                specific_input = (
                    item.input_name.lower() in question_lower
                )

                generic_fertilizer_question = any(
                    word in question_lower
                    for word in ["fertilizer", "fertiliser", "input"]
                )

                if specific_input or generic_fertilizer_question:

                    evidence.append({
                        "type": "input",
                        "name": item.input_name,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "amount": item.cost,
                        "date": item.application_date,
                        "description": item.description
                    })

    # -----------------------------------------------------
    # EXPENSES / SPENDING
    # -----------------------------------------------------

    if expense_intent:

        for crop in selected_crops:

            # ---------------------------------------------
            # INPUT COSTS
            # ---------------------------------------------

            result = await db.execute(
                select(Input)
                .where(Input.crop_id == crop.id)
                .order_by(Input.application_date)
            )

            inputs = result.scalars().all()

            for item in inputs:

                specific_input = (
                    item.input_name.lower() in question_lower
                )

                # If a specific input such as Urea or DAP
                # is mentioned, only return that input.
                if specific_input:

                    evidence.append({
                        "type": "input",
                        "name": item.input_name,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "amount": item.cost,
                        "date": item.application_date,
                        "description": item.description
                    })

                # Generic spending question
                elif not any(
                    name.lower() in question_lower
                    for name in [i.input_name for i in inputs]
                ):

                    evidence.append({
                        "type": "input",
                        "name": item.input_name,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "amount": item.cost,
                        "date": item.application_date,
                        "description": item.description
                    })

            # ---------------------------------------------
            # OTHER EXPENSES
            # ---------------------------------------------

            result = await db.execute(
                select(Expense)
                .where(Expense.crop_id == crop.id)
                .order_by(Expense.expense_date)
            )

            expenses = result.scalars().all()

            for expense in expenses:

                specific_expense = (
                    expense.expense_type.lower() in question_lower
                )

                # Specific expense such as Tractor/Labour
                if specific_expense:

                    evidence.append({
                        "type": "expense",
                        "name": expense.expense_type,
                        "quantity": None,
                        "unit": None,
                        "amount": expense.amount,
                        "date": expense.expense_date,
                        "description": expense.description
                    })

                # Generic spending question
                elif not any(
                    e.expense_type.lower() in question_lower
                    for e in expenses
                ):

                    evidence.append({
                        "type": "expense",
                        "name": expense.expense_type,
                        "quantity": None,
                        "unit": None,
                        "amount": expense.amount,
                        "date": expense.expense_date,
                        "description": expense.description
                    })

    # -----------------------------------------------------
    # HARVEST
    # -----------------------------------------------------

    if harvest_intent or revenue_intent:

        for crop in selected_crops:

            result = await db.execute(
                select(Harvest)
                .where(Harvest.crop_id == crop.id)
                .order_by(Harvest.harvest_date)
            )

            harvests = result.scalars().all()

            for harvest in harvests:

                evidence.append({
                    "type": "harvest",
                    "name": "Harvest",
                    "quantity": harvest.quantity,
                    "unit": harvest.unit,
                    "amount": harvest.selling_price,
                    "date": harvest.harvest_date,
                    "description": harvest.description
                })

    # -----------------------------------------------------
    # ACTIVITIES
    # -----------------------------------------------------

    if activity_intent:

        for crop in selected_crops:

            result = await db.execute(
                select(Activity)
                .where(Activity.crop_id == crop.id)
                .order_by(Activity.activity_date)
            )

            activities = result.scalars().all()

            for activity in activities:

                evidence.append({
                    "type": "activity",
                    "name": activity.activity_type,
                    "quantity": None,
                    "unit": None,
                    "amount": None,
                    "date": activity.activity_date,
                    "description": activity.description
                })

    return evidence


# ---------------------------------------------------------
# FARM DATA FOR AI
# ---------------------------------------------------------

async def get_farm_data_for_ai(
    db: AsyncSession,
    user_id: int,
    question: str
):
    """
    Give Gemini ONLY the records relevant to the question.
    """

    evidence = await get_farm_evidence(
        db=db,
        user_id=user_id,
        question=question
    )

    if not evidence:
        return "No relevant farm records found for this question."

    return str(evidence)


# ---------------------------------------------------------
# OLD FERTILIZER QUERY
# ---------------------------------------------------------

async def fertilizer_query(
    db: AsyncSession,
    crop_name: str,
    user_id: int,
    question: str
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.name.ilike(crop_name),
            Farm.user_id == user_id
        )
    )

    crop = result.scalar_one_or_none()

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    result = await db.execute(
        select(Input)
        .where(
            Input.crop_id == crop.id,
            Input.input_type.ilike("fertilizer")
        )
        .order_by(Input.application_date)
    )

    inputs = result.scalars().all()

    if not inputs:
        return {
            "question": question,
            "answer": f"No fertilizer records found for {crop.name}.",
            "evidence": []
        }

    total_quantity = sum(item.quantity for item in inputs)

    unit = inputs[0].unit

    evidence = []

    for item in inputs:
        evidence.append({
            "type": "input",
            "name": item.input_name,
            "quantity": item.quantity,
            "unit": item.unit,
            "date": item.application_date,
            "description": item.description
        })

    return {
        "question": question,
        "answer": f"You used {total_quantity:g} {unit} of fertilizer on {crop.name}.",
        "evidence": evidence
    }