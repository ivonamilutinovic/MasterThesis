package com.example.trainwiser.network;

import com.example.trainwiser.common.GlobalAPIAccessData;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class APIRetrofitClient {
    private static Retrofit retrofit = null;

    public static Retrofit getAPIClient() {
        if (retrofit == null) {
            retrofit = new Retrofit.Builder()
                    .baseUrl(GlobalAPIAccessData.getBackendUrl() + "api/")
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
}
