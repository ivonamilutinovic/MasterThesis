package com.example.trainwiser.network;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class Oauth2RetrofitClient {
    private static Retrofit retrofit = null;

    public static Retrofit getOauth2Client() {
        if (retrofit == null) {
            retrofit = new Retrofit.Builder()
                    .baseUrl("https://feasible-brightly-cobra.ngrok-free.app/o/")
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
}
