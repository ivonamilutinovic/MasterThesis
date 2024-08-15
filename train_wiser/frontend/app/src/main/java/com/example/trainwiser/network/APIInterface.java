package com.example.trainwiser.network;

import com.example.trainwiser.network.api_models.account.AccountDataResponse;
import com.example.trainwiser.network.api_models.registration.RegisterRequestData;
import com.example.trainwiser.network.api_models.registration.RegisterResponseData;
import com.example.trainwiser.network.api_models.results_prediction.ResultsPredictionResponseData;
import com.example.trainwiser.network.api_models.stats.TrainingStatsResponseData;
import com.example.trainwiser.network.api_models.trainings.TrainingPlanResponse;

import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.PATCH;
import retrofit2.http.POST;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface APIInterface {
    @POST("users/register/")
    Call<RegisterResponseData> registerUser(@Body RegisterRequestData user);

    // Requests with authentication token in header
    @GET("users/me/")
    Call<AccountDataResponse> getAccount(@Header("Authorization") String authorization);

    @PATCH("users/me/")
    Call<AccountDataResponse> updateAccount(@Header("Authorization") String authorization, @Body Map<String, Object> updates);

    @DELETE("users/me/")
    Call<Void> deleteAccount(@Header("Authorization") String authorization);

    @GET("results_prediction/")
    Call<ResultsPredictionResponseData> getResultsPrediction(
            @Header("Authorization") String authorization,
            @Query("race_distance") String race_distance);

    @GET("stats/{year}/{month}/")
    Call<TrainingStatsResponseData> getMonthlyStats(
            @Header("Authorization") String authorization,
            @Path("year") int year,
            @Path("month") int month
    );

    @GET("trainings/")
    Call<Map<String, List<List<List<TrainingPlanResponse>>>>> getTrainingPlan(
            @Header("Authorization") String authorization,
            @Query("goal_time") int goalTime,
            @Query("race_distance") float raceDistance
    );


}
