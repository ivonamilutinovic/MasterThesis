package com.example.trainwiser.network.utils;

import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

import com.example.trainwiser.LoginActivity;
import com.example.trainwiser.Utils;
import com.example.trainwiser.common.GlobalAPIAccessData;
import com.example.trainwiser.common.PreferenceType;
import com.example.trainwiser.common.SharedPreferenceSingleton;
import com.example.trainwiser.network.Oauth2Interface;
import com.example.trainwiser.network.Oauth2RetrofitClient;
import com.example.trainwiser.network.api_models.refresh_token.RefreshTokenRequestData;
import com.example.trainwiser.network.api_models.refresh_token.RefreshTokenResponseData;

import java.net.HttpURLConnection;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class APIUtils {
    public static String getAccessToken(Context ctx) {
        return (String) SharedPreferenceSingleton.getInstance(ctx)
                .getValue(APIKeys.API_ACCESS_TOKEN.toString(), PreferenceType.STRING);
    }

    public static long getExpiresAt(Context ctx) {
        return (Long) SharedPreferenceSingleton.getInstance(ctx)
                .getValue(APIKeys.API_EXPIRES_AT.toString(), PreferenceType.LONG);
    }

    public static String getRefreshToken(Context ctx) {
        return (String) SharedPreferenceSingleton.getInstance(ctx)
                .getValue(APIKeys.API_REFRESH_TOKEN.toString(), PreferenceType.STRING);
    }

    public static void removeAPIKeysData(Context ctx) {
        SharedPreferenceSingleton.getInstance(ctx).removeData(APIKeys.API_ACCESS_TOKEN.toString());
        SharedPreferenceSingleton.getInstance(ctx).removeData(APIKeys.API_EXPIRES_AT.toString());
        SharedPreferenceSingleton.getInstance(ctx).removeData(APIKeys.API_REFRESH_TOKEN.toString());
    }

    public static void refreshAccessTokenIfNeeded(Context ctx, Runnable callbackFunction) {
        String accessToken = getAccessToken(ctx);
        long expiresAt = getExpiresAt(ctx);
        String refreshToken = getRefreshToken(ctx);

        if (accessToken == null || refreshToken == null || expiresAt == Long.MAX_VALUE)
            return;

        long currentTime = Utils.currentTimestampInSeconds();
        int timeDelta = 120;

        if (expiresAt - timeDelta <= currentTime) {

            RefreshTokenRequestData refreshTokenRequestData = new RefreshTokenRequestData("refresh_token",
                    refreshToken,
                    GlobalAPIAccessData.getClientId(),
                    GlobalAPIAccessData.getClientSecret());

            Oauth2RetrofitClient.getOauth2Client().create(Oauth2Interface.class).refreshToken(refreshTokenRequestData).enqueue(new Callback<RefreshTokenResponseData>() {
                @Override
                public void onResponse(Call<RefreshTokenResponseData> call, Response<RefreshTokenResponseData> response) {
                    if (response.code() == HttpURLConnection.HTTP_OK) {
                        if (response.body() != null) {
                            String access_token = response.body().getAccessToken();
                            long expires_in = response.body().getExpiresIn();
                            String refresh_token = response.body().getRefreshToken();

                            SharedPreferenceSingleton sharedPreference = SharedPreferenceSingleton.getInstance(ctx);
                            sharedPreference.setValue(APIKeys.API_ACCESS_TOKEN.toString(), access_token, PreferenceType.STRING);
                            sharedPreference.setValue(APIKeys.API_EXPIRES_AT.toString(), APIUtils.getExpiresAt(expires_in), PreferenceType.LONG);
                            sharedPreference.setValue(APIKeys.API_REFRESH_TOKEN.toString(), refresh_token, PreferenceType.STRING);

                            if (callbackFunction != null)
                                callbackFunction.run();
                        } else {
                            Toast.makeText(ctx, "Response from the backend application is empty", Toast.LENGTH_LONG).show();
                            // todo: add deleting of call stacks to avoid returning to older activity
                            // revoke token!
                            Intent intent = new Intent(ctx, LoginActivity.class);
                            ctx.startActivity(intent);
                        }
                    } else {
                        Utils.onResponseErrorLogging(ctx, response);
                        Intent intent = new Intent(ctx, LoginActivity.class);
                        ctx.startActivity(intent);
                        Utils.onResponseErrorLogging(ctx, response);
                    }
                }

                @Override
                public void onFailure(Call<RefreshTokenResponseData> call, Throwable t) {
                    Utils.onFailureLogging(ctx, t);
                    Intent intent = new Intent(ctx, LoginActivity.class);
                    ctx.startActivity(intent);
                }
            });
        } else {
            if (callbackFunction != null)
                callbackFunction.run();
        }
    }

    public static long getExpiresAt(long expiresIn) {
        return Utils.currentTimestampInSeconds() + expiresIn;

    }

    public static String getAuthorizationHeader(Context ctx) {
        String accessToken = APIUtils.getAccessToken(ctx);
        return "Bearer " + accessToken;
    }
}