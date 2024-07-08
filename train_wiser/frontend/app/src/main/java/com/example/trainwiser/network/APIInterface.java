package com.example.trainwiser.network;
import com.example.trainwiser.network.api_models.RegisterRequestData;
import com.example.trainwiser.network.api_models.RegisterResponseData;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface APIInterface {

    @POST("users/register/")
    Call<RegisterResponseData> registerUser(@Body RegisterRequestData user);


}
