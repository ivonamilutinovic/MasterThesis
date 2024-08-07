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
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface APIInterfaceWithInterceptorForTokens {
    @GET("users/me/")
    Call<AccountDataResponse> getAccount();

    @PATCH("users/me/")
    Call<AccountDataResponse> updateAccount(@Body Map<String, Object> updates);

    @DELETE("users/me/")
    Call<Void> deleteAccount();

    @POST("results_prediction/")
    Call<ResultsPredictionResponseData> getResultsPrediction(@Body ResultsPredictionRequestData resultsPredictionRequestData);

//    @GET("api/training/")
//    Call<MonthlyStatsResponse> getMonthlyStats(Float race_distance, Integer goal_in_seconds);


//    @GET("api/stats/")
//    Call<MonthlyStatsResponse> getMonthlyStats(@Path("month") String month);

}
