package com.example.agriai.data.repository

import com.example.agriai.data.model.QueryRequest
import com.example.agriai.data.model.QueryResponse
import com.example.agriai.data.network.ApiService
import com.example.agriai.data.network.NetworkResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class AIRepository(private val apiService: ApiService) {
    fun queryAI(question: String): Flow<NetworkResult<QueryResponse>> = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.queryAI(QueryRequest(question))
            if (response.isSuccessful && response.body() != null) {
                emit(NetworkResult.Success(response.body()!!))
            } else {
                emit(NetworkResult.Error(response.message()))
            }
        } catch (e: Exception) {
            emit(NetworkResult.Error(e.message ?: "AI Query failed"))
        }
    }
}
