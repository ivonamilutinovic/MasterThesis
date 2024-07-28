package com.example.trainwiser.network;

import com.example.trainwiser.network.api_models.account.AccountDataResponse;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Header;

public interface APIInterfaceWithInterceptorForTokens {
    @GET("users/me/")
    Call<AccountDataResponse> getAccount();
}
