package com.example.trainwiser.network.utils;

import android.content.Context;

import com.example.trainwiser.R;
import com.example.trainwiser.Utils;
import com.example.trainwiser.common.PreferenceType;
import com.example.trainwiser.common.SharedPreferenceSingleton;

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

    private static void refreshAccessTokenIfNeeded(Context ctx){
        String accessToken = getAccessToken(ctx);
        long expiresAt = getExpiresAt(ctx);
        String refreshToken = getRefreshToken(ctx);

        if(accessToken == null || refreshToken == null || expiresAt == Long.MAX_VALUE)
            return;

        long currentTime = Utils.currentTimestampInSeconds();
        int timeDelta = 30 * 60;

        if (expiresAt - timeDelta <= currentTime) {
            

        }
    }
}
