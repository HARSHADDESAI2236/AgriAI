package com.example.agriai.data.repository

import com.example.agriai.data.model.*
import com.example.agriai.data.network.ApiService
import com.example.agriai.data.network.NetworkResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class FarmRepository(private val apiService: ApiService) {

    // --- Farm ---
    fun getFarms(): Flow<NetworkResult<List<FarmResponse>>> = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getFarms()
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createFarm(farm: CreateFarm) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createFarm(farm)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun getFarm(id: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getFarm(id)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- Fields ---
    fun getFieldsForFarm(farmId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getFieldsForFarm(farmId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createField(field: CreateField) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createField(field)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- Seasons ---
    fun getSeasonsForField(fieldId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getSeasonsForField(fieldId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createSeason(season: CreateSeason) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createSeason(season)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- Crops ---
    fun getCropsForSeason(seasonId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getCropsForSeason(seasonId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createCrop(crop: CreateCrop) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createCrop(crop)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }
    
    fun getCrop(cropId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getCrop(cropId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- Activities ---
    fun getActivitiesForCrop(cropId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getActivitiesForCrop(cropId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createActivity(activity: CreateActivity) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createActivity(activity)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- Inputs ---
    fun getInputsForCrop(cropId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getInputsForCrop(cropId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createInput(input: CreateInput) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createInput(input)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- Expenses ---
    fun getExpensesForCrop(cropId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getExpensesForCrop(cropId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createExpense(expense: CreateExpense) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createExpense(expense)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- Harvests ---
    fun getHarvestsForCrop(cropId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getHarvestsForCrop(cropId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body() ?: emptyList()))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    fun createHarvest(harvest: CreateHarvest) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.createHarvest(harvest)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }

    // --- History ---
    fun getCropHistory(cropId: Int) = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getCropHistory(cropId)
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }
    
    // Health & Root
    fun checkHealth() = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.getHealth()
            if (response.isSuccessful) emit(NetworkResult.Success(response.body()!!))
            else emit(NetworkResult.Error(response.message()))
        } catch (e: Exception) { emit(NetworkResult.Error(e.message ?: "Error")) }
    }
}
