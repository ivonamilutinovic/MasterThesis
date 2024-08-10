package com.example.trainwiser.network;

import com.example.trainwiser.network.api_models.account.AccountDataResponse;
import com.example.trainwiser.network.api_models.results_prediction.ResultsPredictionResponseData;
import com.example.trainwiser.network.api_models.stats.TrainingStatsResponseData;
import com.example.trainwiser.network.api_models.trainings.TrainingResponseData;

import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.PATCH;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface APIInterfaceWithInterceptorForTokens {
    @GET("users/me/")
    Call<AccountDataResponse> getAccount();

    @PATCH("users/me/")
    Call<AccountDataResponse> updateAccount(@Body Map<String, Object> updates);

    @DELETE("users/me/")
    Call<Void> deleteAccount();

    @GET("results_prediction/")
    Call<ResultsPredictionResponseData> getResultsPrediction(
            @Query("race_distance") String race_distance);

    @GET("stats/{year}/{month}/")
    Call<TrainingStatsResponseData> getMonthlyStats(
            @Path("year") int year,
            @Path("month") int month
    );

    @GET("trainings/")
    Call<List<List<List<TrainingResponseData>>>> getTrainingSuggestions(
            @Query("goal_time") int goalTime,
            @Query("race_distance") float raceDistance
    );
}
