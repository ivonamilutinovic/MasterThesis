package com.example.trainwiser.common;

import android.content.Context;
import android.content.SharedPreferences;


public class SharedPreferenceSingleton {
    private static SharedPreferenceSingleton instance;
    private final SharedPreferences sharedPreference;

    private SharedPreferenceSingleton(Context context) {
        sharedPreference = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE);
    }

    public static synchronized SharedPreferenceSingleton getInstance(Context context) {
        if (instance == null) {
            instance = new SharedPreferenceSingleton(context);
        }
        return instance;
    }

    public Object getValue(String key, PreferenceType preferenceType) {
        switch (preferenceType) {
            case INTEGER:
                return sharedPreference.getInt(key, Integer.MAX_VALUE);
            case STRING:
                return sharedPreference.getString(key, null);
            case LONG:
                return sharedPreference.getLong(key, Long.MAX_VALUE);
            default:
                return null;
        }
    }

    public void setValue(String key, Object value, PreferenceType preferenceType) {
        SharedPreferences.Editor editor = sharedPreference.edit();

        switch (preferenceType){
            case INTEGER:
                editor.putInt(key, (Integer) value);
                break;
            case STRING:
                editor.putString(key, (String) value);
                break;
            case LONG:
                editor.putLong(key, (Long) value);
            default:
                break;
        }

        editor.apply();
    }

    public void removeData(String key)
    {
        sharedPreference.edit().remove(key).apply();
    }
}
