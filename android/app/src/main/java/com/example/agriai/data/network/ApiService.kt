package com.example.agriai.data.network

import com.example.agriai.data.model.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // --- USER APIs ---
    @POST("users/")
    suspend fun register(@Body user: CreateUser): Response<UserResponse>

    @POST("users/login")
    suspend fun login(@Body credentials: LoginUser): Response<Token>

    @PUT("users/{user_id}")
    suspend fun updateUser(@Path("user_id") userId: Int, @Body user: UpdateUser): Response<UserResponse>

    @DELETE("users/{user_id}")
    suspend fun deleteUser(@Path("user_id") userId: Int): Response<Unit>

    @FormUrlEncoded
    @POST("users/token")
    suspend fun getAccessToken(
        @Field("username") email: String,
        @Field("password") pass: String
    ): Response<Token>

    // --- FARM APIs ---
    @GET("farms/")
    suspend fun getFarms(): Response<List<FarmResponse>>

    @POST("farms/")
    suspend fun createFarm(@Body farm: CreateFarm): Response<FarmResponse>

    @GET("farms/{farm_id}")
    suspend fun getFarm(@Path("farm_id") farmId: Int): Response<FarmResponse>

    @PUT("farms/{farm_id}")
    suspend fun updateFarm(@Path("farm_id") farmId: Int, @Body farm: UpdateFarm): Response<FarmResponse>

    @DELETE("farms/{farm_id}")
    suspend fun deleteFarm(@Path("farm_id") farmId: Int): Response<Unit>

    // --- FIELD APIs ---
    @POST("fields/")
    suspend fun createField(@Body field: CreateField): Response<FieldResponse>

    @GET("fields/farm/{farm_id}")
    suspend fun getFieldsForFarm(@Path("farm_id") farmId: Int): Response<List<FieldResponse>>

    @GET("fields/{field_id}")
    suspend fun getField(@Path("field_id") fieldId: Int): Response<FieldResponse>

    @PUT("fields/{field_id}")
    suspend fun updateField(@Path("field_id") fieldId: Int, @Body field: UpdateField): Response<FieldResponse>

    @DELETE("fields/{field_id}")
    suspend fun deleteField(@Path("field_id") fieldId: Int): Response<Unit>

    // --- SEASON APIs ---
    @POST("seasons/")
    suspend fun createSeason(@Body season: CreateSeason): Response<SeasonResponse>

    @GET("seasons/field/{field_id}")
    suspend fun getSeasonsForField(@Path("field_id") fieldId: Int): Response<List<SeasonResponse>>

    @GET("seasons/{season_id}")
    suspend fun getSeason(@Path("season_id") seasonId: Int): Response<SeasonResponse>

    @PUT("seasons/{season_id}")
    suspend fun updateSeason(@Path("season_id") seasonId: Int, @Body season: UpdateSeason): Response<SeasonResponse>

    @DELETE("seasons/{season_id}")
    suspend fun deleteSeason(@Path("season_id") seasonId: Int): Response<Unit>

    // --- CROP APIs ---
    @POST("crops/")
    suspend fun createCrop(@Body crop: CreateCrop): Response<CropResponse>

    @GET("crops/season/{season_id}")
    suspend fun getCropsForSeason(@Path("season_id") seasonId: Int): Response<List<CropResponse>>

    @GET("crops/{crop_id}")
    suspend fun getCrop(@Path("crop_id") cropId: Int): Response<CropResponse>

    @PUT("crops/{crop_id}")
    suspend fun updateCrop(@Path("crop_id") cropId: Int, @Body crop: UpdateCrop): Response<CropResponse>

    @DELETE("crops/{crop_id}")
    suspend fun deleteCrop(@Path("crop_id") cropId: Int): Response<Unit>

    // --- ACTIVITY APIs ---
    @POST("activities/")
    suspend fun createActivity(@Body activity: CreateActivity): Response<ActivityResponse>

    @GET("activities/crop/{crop_id}")
    suspend fun getActivitiesForCrop(@Path("crop_id") cropId: Int): Response<List<ActivityResponse>>

    @GET("activities/{activity_id}")
    suspend fun getActivity(@Path("activity_id") activityId: Int): Response<ActivityResponse>

    @PUT("activities/{activity_id}")
    suspend fun updateActivity(@Path("activity_id") activityId: Int, @Body activity: UpdateActivity): Response<ActivityResponse>

    @DELETE("activities/{activity_id}")
    suspend fun deleteActivity(@Path("activity_id") activityId: Int): Response<Unit>

    // --- INPUT APIs ---
    @POST("inputs/")
    suspend fun createInput(@Body input: CreateInput): Response<InputResponse>

    @GET("inputs/crop/{crop_id}")
    suspend fun getInputsForCrop(@Path("crop_id") cropId: Int): Response<List<InputResponse>>

    @GET("inputs/{input_id}")
    suspend fun getInput(@Path("input_id") inputId: Int): Response<InputResponse>

    @PUT("inputs/{input_id}")
    suspend fun updateInput(@Path("input_id") inputId: Int, @Body input: UpdateInput): Response<InputResponse>

    @DELETE("inputs/{input_id}")
    suspend fun deleteInput(@Path("input_id") inputId: Int): Response<Unit>

    // --- EXPENSE APIs ---
    @POST("expenses/")
    suspend fun createExpense(@Body expense: CreateExpense): Response<ExpenseResponse>

    @GET("expenses/crop/{crop_id}")
    suspend fun getExpensesForCrop(@Path("crop_id") cropId: Int): Response<List<ExpenseResponse>>

    @GET("expenses/{expense_id}")
    suspend fun getExpense(@Path("expense_id") expenseId: Int): Response<ExpenseResponse>

    @PUT("expenses/{expense_id}")
    suspend fun updateExpense(@Path("expense_id") expenseId: Int, @Body expense: UpdateExpense): Response<ExpenseResponse>

    @DELETE("expenses/{expense_id}")
    suspend fun deleteExpense(@Path("expense_id") expenseId: Int): Response<Unit>

    // --- HARVEST APIs ---
    @POST("harvests/")
    suspend fun createHarvest(@Body harvest: CreateHarvest): Response<HarvestResponse>

    @GET("harvests/crop/{crop_id}")
    suspend fun getHarvestsForCrop(@Path("crop_id") cropId: Int): Response<List<HarvestResponse>>

    @GET("harvests/{harvest_id}")
    suspend fun getHarvest(@Path("harvest_id") harvestId: Int): Response<HarvestResponse>

    @PUT("harvests/{harvest_id}")
    suspend fun updateHarvest(@Path("harvest_id") harvestId: Int, @Body harvest: UpdateHarvest): Response<HarvestResponse>

    @DELETE("harvests/{harvest_id}")
    suspend fun deleteHarvest(@Path("harvest_id") harvestId: Int): Response<Unit>

    // --- HISTORY API ---
    @GET("history/crop/{crop_id}")
    suspend fun getCropHistory(@Path("crop_id") cropId: Int): Response<CropHistoryResponse>

    // --- AI QUERY API ---
    @POST("query/")
    suspend fun queryAI(@Body request: QueryRequest): Response<QueryResponse>

    // --- ROOT & HEALTH ---
    @GET("/")
    suspend fun getRoot(): Response<RootResponse>

    @GET("health")
    suspend fun getHealth(): Response<HealthResponse>
}
