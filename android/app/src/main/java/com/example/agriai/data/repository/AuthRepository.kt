package com.example.agriai.data.repository

import com.example.agriai.data.local.TokenManager
import com.example.agriai.data.model.*
import com.example.agriai.data.network.ApiService
import com.example.agriai.data.network.NetworkResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.map
import retrofit2.Response

class AuthRepository(
    private val apiService: ApiService,
    private val tokenManager: TokenManager
) {
    fun login(credentials: LoginUser): Flow<NetworkResult<Token>> = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.login(credentials)
            if (response.isSuccessful && response.body() != null) {
                val token = response.body()!!
                tokenManager.saveToken(token.accessToken)
                emit(NetworkResult.Success(token))
            } else {
                emit(NetworkResult.Error("Login failed: ${response.message()}"))
            }
        } catch (e: Exception) {
            emit(NetworkResult.Error(e.message ?: "Unknown error occurred"))
        }
    }

    fun register(user: CreateUser): Flow<NetworkResult<UserResponse>> = flow {
        emit(NetworkResult.Loading())
        try {
            val response = apiService.register(user)
            if (response.isSuccessful && response.body() != null) {
                emit(NetworkResult.Success(response.body()!!))
            } else {
                emit(NetworkResult.Error("Registration failed: ${response.message()}"))
            }
        } catch (e: Exception) {
            emit(NetworkResult.Error(e.message ?: "Unknown error occurred"))
        }
    }

    suspend fun logout() {
        tokenManager.clearSession()
    }

    val isLoggedIn: Flow<Boolean> = tokenManager.token.map { it != null }

    val token: Flow<String?> = tokenManager.token
}
