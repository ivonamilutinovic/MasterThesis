package com.example.trainwiser;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import com.example.trainwiser.network.utils.APIUtils;

import org.json.JSONObject;

import java.time.Instant;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import okhttp3.ResponseBody;
import retrofit2.Response;

public class Utils {
    public static final Map<String, Integer> activityEmojisMap = new HashMap<>();

    static {
        activityEmojisMap.put("Run", R.string.run_emoji);
        activityEmojisMap.put("Ride", R.string.ride_emoji);
        activityEmojisMap.put("VirtualRide", R.string.ride_emoji);
        activityEmojisMap.put("Swim", R.string.swim_emoji);
        activityEmojisMap.put("WeightTraining", R.string.weight_training_emoji);
        activityEmojisMap.put("RestDay", R.string.rest_day_emoji);
    }

    public static String getActivityEmoji(Context context, String activityType) {
        int emojiResId = activityEmojisMap.getOrDefault(activityType, -1);
        if (emojiResId == -1){
            return activityType;
        }
        return context.getString(emojiResId);
    }

    public static long currentTimestampInSeconds() {
        return Instant.now().getEpochSecond();
    }

    public static String secondsInFormatedTime(Integer seconds) {
        if (seconds == null)
            return "00:00:00";

        int hours = seconds / 3600;
        int remainder = seconds % 3600;
        int minutes = remainder / 60;
        seconds = remainder % 60;

        return String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds);
    }

    public static void onResponseErrorLogging(Context ctx, Response<?> response) {
        if (response.code() == 401){
            String errorMessage = "Session issues, please log in again";
            Log.e("API Response Error", errorMessage);
            Toast.makeText(ctx, errorMessage, Toast.LENGTH_LONG).show();
            return;
        }

        if (response.code() == 500){
            String errorMessage = "Internal server error";
            Log.e("API Response Error", errorMessage);
            Toast.makeText(ctx, errorMessage, Toast.LENGTH_LONG).show();
            return;
        }

        ResponseBody errorBody = response.errorBody();
        String defaultErrorMessage = "Unknown error - " + response.code();
        String errorMessage = defaultErrorMessage;
        if (errorBody != null){
            String errorBodyStr;
            JSONObject errorBodyJson;

            try {
                errorBodyStr = errorBody.string();
                errorBodyJson = new JSONObject(errorBodyStr);
                errorMessage = errorBodyJson.optString("error_description");
                if (errorMessage.equals(""))
                    errorMessage = errorBodyJson.optString("error");
                if (errorMessage.equals(""))
                    errorMessage = errorBodyStr;
            } catch (Exception ignored) {
            }
        }
        Log.e("API Response Error", errorMessage);
        Toast.makeText(ctx, errorMessage, Toast.LENGTH_LONG).show();
    }

    public static void onFailureLogging(Context ctx, Throwable t) {
        String errorMessage = "Error: " + t.getClass().getSimpleName() + " - " + t.getMessage();
        Log.e("API Failure", errorMessage);
        Toast.makeText(ctx, errorMessage, Toast.LENGTH_LONG).show();
    }
}
