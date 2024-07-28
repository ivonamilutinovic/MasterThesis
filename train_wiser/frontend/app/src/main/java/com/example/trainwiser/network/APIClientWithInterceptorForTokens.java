package com.example.trainwiser.network;

import android.content.Context;

import com.example.trainwiser.common.GlobalAPIAccessData;
import com.example.trainwiser.network.utils.APIUtils;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class APIClientWithInterceptorForTokens {
    private static Retrofit retrofit = null;

    public static Retrofit getAPIClient(Context ctx) {
        String accessToken = APIUtils.getAccessToken(ctx);
        OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .addInterceptor(chain -> {
                    Request original = chain.request();
                    Request request = original.newBuilder()
                            .header("Authorization", "Bearer " + accessToken)
                            .build();
                    return chain.proceed(request);
                })
                .build();

        if (retrofit == null) {
            retrofit = new Retrofit.Builder()
                    .baseUrl(GlobalAPIAccessData.getBackendUrl() + "api/")
                    .client(okHttpClient)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }

}
