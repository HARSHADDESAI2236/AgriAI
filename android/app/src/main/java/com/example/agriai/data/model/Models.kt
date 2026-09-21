package com.example.agriai.data.model

import com.google.gson.annotations.SerializedName

// User Models
data class CreateUser(
    val username: String,
    val email: String,
    val password: String
)

data class LoginUser(
    val email: String,
    val password: String
)

data class UpdateUser(
    val username: String? = null,
    val email: String? = null
)

data class UserResponse(
    val id: Int,
    val username: String,
    val email: String
)

data class Token(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("token_type") val tokenType: String
)

// Farm Models
data class CreateFarm(
    @SerializedName("farm_name") val farmName: String,
    val location: String,
    @SerializedName("total_area") val totalArea: Float,
    @SerializedName("area_unit") val areaUnit: String
)

data class UpdateFarm(
    @SerializedName("farm_name") val farmName: String? = null,
    val location: String? = null,
    @SerializedName("total_area") val totalArea: Float? = null,
    @SerializedName("area_unit") val areaUnit: String? = null
)

data class FarmResponse(
    val id: Int,
    @SerializedName("owner_id") val ownerId: Int,
    @SerializedName("farm_name") val farmName: String,
    val location: String,
    @SerializedName("total_area") val totalArea: Float,
    @SerializedName("area_unit") val areaUnit: String
)

// Field Models
data class CreateField(
    @SerializedName("farm_id") val farmId: Int,
    @SerializedName("field_name") val fieldName: String,
    val area: Float
)

data class UpdateField(
    @SerializedName("field_name") val fieldName: String? = null,
    val area: Float? = null
)

data class FieldResponse(
    val id: Int,
    @SerializedName("farm_id") val farmId: Int,
    @SerializedName("field_name") val fieldName: String,
    val area: Float
)

// Season Models
data class CreateSeason(
    @SerializedName("field_id") val fieldId: Int,
    @SerializedName("season_name") val seasonName: String,
    @SerializedName("start_date") val startDate: String,
    @SerializedName("end_date") val endDate: String
)

data class UpdateSeason(
    @SerializedName("season_name") val seasonName: String? = null,
    @SerializedName("start_date") val startDate: String? = null,
    @SerializedName("end_date") val endDate: String? = null
)

data class SeasonResponse(
    val id: Int,
    @SerializedName("field_id") val fieldId: Int,
    @SerializedName("season_name") val seasonName: String,
    @SerializedName("start_date") val startDate: String,
    @SerializedName("end_date") val endDate: String
)

// Crop Models
data class CreateCrop(
    @SerializedName("season_id") val seasonId: Int,
    @SerializedName("crop_name") val cropName: String,
    val variety: String,
    @SerializedName("sowing_date") val sowingDate: String,
    @SerializedName("harvest_date") val harvestDate: String? = null
)

data class UpdateCrop(
    @SerializedName("crop_name") val cropName: String? = null,
    val variety: String? = null,
    @SerializedName("sowing_date") val sowingDate: String? = null,
    @SerializedName("harvest_date") val harvestDate: String? = null
)

data class CropResponse(
    val id: Int,
    @SerializedName("season_id") val seasonId: Int,
    @SerializedName("crop_name") val cropName: String,
    val variety: String,
    @SerializedName("sowing_date") val sowingDate: String,
    @SerializedName("harvest_date") val harvestDate: String? = null
)

// Activity Models
data class CreateActivity(
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("activity_type") val activityType: String,
    @SerializedName("activity_date") val activityDate: String,
    val description: String
)

data class UpdateActivity(
    @SerializedName("activity_type") val activityType: String? = null,
    @SerializedName("activity_date") val activityDate: String? = null,
    val description: String? = null
)

data class ActivityResponse(
    val id: Int,
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("activity_type") val activityType: String,
    @SerializedName("activity_date") val activityDate: String,
    val description: String
)

// Input Models
data class CreateInput(
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("input_name") val inputName: String,
    @SerializedName("input_type") val inputType: String,
    val quantity: Float,
    val unit: String,
    @SerializedName("application_date") val applicationDate: String,
    val cost: Float,
    val description: String
)

data class UpdateInput(
    @SerializedName("input_name") val inputName: String? = null,
    @SerializedName("input_type") val inputType: String? = null,
    val quantity: Float? = null,
    val unit: String? = null,
    @SerializedName("application_date") val applicationDate: String? = null,
    val cost: Float? = null,
    val description: String? = null
)

data class InputResponse(
    val id: Int,
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("input_name") val inputName: String,
    @SerializedName("input_type") val inputType: String,
    val quantity: Float,
    val unit: String,
    @SerializedName("application_date") val applicationDate: String,
    val cost: Float,
    val description: String
)

// Expense Models
data class CreateExpense(
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("expense_type") val expenseType: String,
    val amount: Float,
    @SerializedName("expense_date") val expenseDate: String,
    val description: String
)

data class UpdateExpense(
    @SerializedName("expense_type") val expenseType: String? = null,
    val amount: Float? = null,
    @SerializedName("expense_date") val expenseDate: String? = null,
    val description: String? = null
)

data class ExpenseResponse(
    val id: Int,
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("expense_type") val expenseType: String,
    val amount: Float,
    @SerializedName("expense_date") val expenseDate: String,
    val description: String
)

// Harvest Models
data class CreateHarvest(
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("harvest_date") val harvestDate: String,
    val quantity: Float,
    val unit: String,
    @SerializedName("selling_price") val sellingPrice: Float,
    val description: String
)

data class UpdateHarvest(
    @SerializedName("harvest_date") val harvestDate: String? = null,
    val quantity: Float? = null,
    val unit: String? = null,
    @SerializedName("selling_price") val sellingPrice: Float? = null,
    val description: String? = null
)

data class HarvestResponse(
    val id: Int,
    @SerializedName("crop_id") val cropId: Int,
    @SerializedName("harvest_date") val harvestDate: String,
    val quantity: Float,
    val unit: String,
    @SerializedName("selling_price") val sellingPrice: Float,
    val description: String
)

// History Models
data class CropHistoryResponse(
    val crop: CropResponse,
    val season: SeasonResponse,
    val activities: List<ActivityResponse>,
    val inputs: List<InputResponse>,
    val expenses: List<ExpenseResponse>,
    val harvests: List<HarvestResponse>
)

// AI Models
data class QueryRequest(
    val question: String
)

data class QueryResponse(
    val question: String,
    val answer: String,
    val evidence: List<EvidenceItem>
)

data class EvidenceItem(
    @SerializedName("input_name") val inputName: String? = null,
    @SerializedName("activity_type") val activityType: String? = null,
    val quantity: Float? = null,
    val unit: String? = null,
    val cost: Float? = null,
    val date: String? = null,
    val description: String? = null
)

data class HealthResponse(
    val status: String
)

data class RootResponse(
    val message: String
)
