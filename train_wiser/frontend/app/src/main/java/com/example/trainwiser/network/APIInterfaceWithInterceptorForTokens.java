package com.example.trainwiser.network;

import com.example.trainwiser.network.api_models.account.AccountDataResponse;
import com.example.trainwiser.network.api_models.results_prediction.ResultsPredictionRequestData;
import com.example.trainwiser.network.api_models.results_prediction.ResultsPredictionResponseData;

import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.PATCH;

public interface APIInterfaceWithInterceptorForTokens {
    @GET("users/me/")
    Call<AccountDataResponse> getAccount();

    @PATCH("users/me/")
    Call<AccountDataResponse> updateAccount(@Body Map<String, Object> updates);

    @DELETE("users/me/")
    Call<Void> deleteAccount();

    @GET("api/result_prediction/")
    Call<ResultsPredictionResponseData> getResultsPrediction(ResultsPredictionRequestData resultsPredictionRequestData);

}
