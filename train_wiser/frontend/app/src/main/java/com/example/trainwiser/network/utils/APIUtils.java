package com.example.trainwiser.network.utils;

import android.content.Context;

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
}
