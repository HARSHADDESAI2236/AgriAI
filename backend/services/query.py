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


# =========================================================
# FIND USER'S CROPS
# =========================================================

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


# =========================================================
# FIND RELEVANT CROPS
# =========================================================

def select_crops(crops, question: str):

    question_lower = question.lower()

    mentioned_crops = []

    for crop in crops:

        if crop.name.lower() in question_lower:
            mentioned_crops.append(crop)

    if mentioned_crops:
        return mentioned_crops

    return crops


# =========================================================
# REMOVE DUPLICATE EVIDENCE
# =========================================================

def remove_duplicate_evidence(evidence):

    unique_evidence = []
    seen = set()

    for item in evidence:

        key = (
            item.get("type"),
            item.get("name"),
            item.get("quantity"),
            item.get("unit"),
            item.get("amount"),
            item.get("date"),
            item.get("description")
        )

        if key not in seen:

            seen.add(key)
            unique_evidence.append(item)

    return unique_evidence


# =========================================================
# GET RELEVANT FARM EVIDENCE
# =========================================================

async def get_farm_evidence(
    db: AsyncSession,
    user_id: int,
    question: str
):

    question_lower = question.lower()

    # =====================================================
    # GET USER CROPS
    # =====================================================

    crops = await get_user_crops(
        db=db,
        user_id=user_id
    )

    if not crops:
        return []

    # =====================================================
    # SELECT CROPS
    # =====================================================

    selected_crops = select_crops(
        crops=crops,
        question=question
    )

    evidence = []

    # =====================================================
    # INTENTS
    # =====================================================

    fertilizer_intent = any(
        word in question_lower
        for word in [
            "fertilizer",
            "fertiliser",
            "urea",
            "dap"
        ]
    )

    expense_intent = any(
        word in question_lower
        for word in [
            "spend",
            "spent",
            "expense",
            "expenses",
            "cost",
            "costs"
        ]
    )

    harvest_intent = any(
        word in question_lower
        for word in [
            "harvest",
            "harvested",
            "yield",
            "produce",
            "production"
        ]
    )

    revenue_intent = any(
        word in question_lower
        for word in [
            "earn",
            "earned",
            "earning",
            "revenue",
            "income",
            "sold",
            "selling",
            "money from"
        ]
    )

    activity_intent = any(
        word in question_lower
        for word in [
            "activity",
            "activities",
            "work",
            "worked",
            "performed"
        ]
    )

    # =====================================================
    # NO INTENT
    # =====================================================

    if not any([
        fertilizer_intent,
        expense_intent,
        harvest_intent,
        revenue_intent,
        activity_intent
    ]):

        return []

    # =====================================================
    # FERTILIZER / INPUT
    # =====================================================

    if fertilizer_intent:

        for crop in selected_crops:

            # -------------------------------------------------
            # IMPORTANT:
            # Do NOT filter by input_type here.
            #
            # This restores the database behavior that was
            # previously working.
            # -------------------------------------------------

            result = await db.execute(
                select(Input)
                .where(
                    Input.crop_id == crop.id
                )
                .order_by(Input.application_date)
            )

            inputs = result.scalars().all()

            if not inputs:
                continue

            # -------------------------------------------------
            # CHECK SPECIFIC FERTILIZER
            #
            # Example:
            # "How much Urea did I use?"
            # -------------------------------------------------

            specific_input_requested = any(
                item.input_name
                and item.input_name.lower() in question_lower
                for item in inputs
            )

            # -------------------------------------------------
            # ADD INPUT EVIDENCE
            # -------------------------------------------------

            for item in inputs:

                if specific_input_requested:

                    if (
                        not item.input_name
                        or item.input_name.lower()
                        not in question_lower
                    ):
                        continue

                evidence.append({
                    "type": "input",
                    "name": item.input_name,
                    "quantity": item.quantity,
                    "unit": item.unit,
                    "amount": item.cost,
                    "date": item.application_date,
                    "description": item.description
                })

    # =====================================================
    # NORMAL EXPENSES
    # =====================================================

    # Do NOT process this section when the question is about
    # fertilizer.
    #
    # Fertilizer cost is already stored in Input.cost.
    #
    # This prevents duplicate fertilizer costs.
    # =====================================================

    if expense_intent and not fertilizer_intent:

        for crop in selected_crops:

            # -------------------------------------------------
            # INPUT COSTS
            # -------------------------------------------------

            result = await db.execute(
                select(Input)
                .where(
                    Input.crop_id == crop.id
                )
                .order_by(Input.application_date)
            )

            inputs = result.scalars().all()

            specific_input_requested = any(
                item.input_name
                and item.input_name.lower() in question_lower
                for item in inputs
            )

            for item in inputs:

                if specific_input_requested:

                    if (
                        not item.input_name
                        or item.input_name.lower()
                        not in question_lower
                    ):
                        continue

                evidence.append({
                    "type": "input",
                    "name": item.input_name,
                    "quantity": item.quantity,
                    "unit": item.unit,
                    "amount": item.cost,
                    "date": item.application_date,
                    "description": item.description
                })

            # -------------------------------------------------
            # EXPENSE TABLE
            # -------------------------------------------------

            result = await db.execute(
                select(Expense)
                .where(
                    Expense.crop_id == crop.id
                )
                .order_by(Expense.expense_date)
            )

            expenses = result.scalars().all()

            specific_expense_requested = any(
                expense.expense_type
                and expense.expense_type.lower()
                in question_lower
                for expense in expenses
            )

            for expense in expenses:

                if specific_expense_requested:

                    if (
                        not expense.expense_type
                        or expense.expense_type.lower()
                        not in question_lower
                    ):
                        continue

                evidence.append({
                    "type": "expense",
                    "name": expense.expense_type,
                    "quantity": None,
                    "unit": None,
                    "amount": expense.amount,
                    "date": expense.expense_date,
                    "description": expense.description
                })

    # =====================================================
    # HARVEST
    # =====================================================

    if harvest_intent or revenue_intent:

        for crop in selected_crops:

            result = await db.execute(
                select(Harvest)
                .where(
                    Harvest.crop_id == crop.id
                )
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

    # =====================================================
    # ACTIVITIES
    # =====================================================

    if activity_intent:

        for crop in selected_crops:

            result = await db.execute(
                select(Activity)
                .where(
                    Activity.crop_id == crop.id
                )
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

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    return remove_duplicate_evidence(evidence)


# =========================================================
# DATA SENT TO AI
# =========================================================

async def get_farm_data_for_ai(
    db: AsyncSession,
    user_id: int,
    question: str
):

    evidence = await get_farm_evidence(
        db=db,
        user_id=user_id,
        question=question
    )

    if not evidence:

        return "No relevant farm records found for this question."

    return str(evidence)


# =========================================================
# DIRECT FERTILIZER QUERY
# =========================================================

async def fertilizer_query(
    db: AsyncSession,
    crop_name: str,
    user_id: int,
    question: str
):

    # -----------------------------------------------------
    # FIND CROP
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # GET ALL INPUTS
    # -----------------------------------------------------

    result = await db.execute(
        select(Input)
        .where(
            Input.crop_id == crop.id
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

    # -----------------------------------------------------
    # FERTILIZER NAMES
    # -----------------------------------------------------

    fertilizer_names = []

    for item in inputs:

        if item.input_name:

            if item.input_name not in fertilizer_names:

                fertilizer_names.append(
                    item.input_name
                )

    # -----------------------------------------------------
    # TOTAL QUANTITY
    # -----------------------------------------------------

    total_quantity = sum(
        item.quantity
        for item in inputs
        if item.quantity is not None
    )

    # -----------------------------------------------------
    # BUILD NAME TEXT
    # -----------------------------------------------------

    if len(fertilizer_names) == 1:

        names_text = fertilizer_names[0]

    elif len(fertilizer_names) == 2:

        names_text = (
            f"{fertilizer_names[0]} "
            f"and {fertilizer_names[1]}"
        )

    else:

        names_text = (
            ", ".join(fertilizer_names[:-1])
            + f", and {fertilizer_names[-1]}"
        )

    # -----------------------------------------------------
    # EVIDENCE
    # -----------------------------------------------------

    evidence = []

    for item in inputs:

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
    # RESPONSE
    # -----------------------------------------------------

    return {
        "question": question,
        "answer": (
            f"You used {names_text} on {crop.name}. "
            f"The total quantity was "
            f"{total_quantity:g} {inputs[0].unit}."
        ),
        "evidence": evidence
    }