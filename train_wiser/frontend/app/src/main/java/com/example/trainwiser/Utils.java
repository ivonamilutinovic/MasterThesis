package com.example.trainwiser;

import java.time.Instant;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import android.content.Context;

public class Utils {
    public static final Map<String, Integer> activityEmojisMap = new HashMap<>();

    static {
        activityEmojisMap.put("Run", R.string.run_emoji); // 🏃
        activityEmojisMap.put("Ride", R.string.ride_emoji); // 🚲
        activityEmojisMap.put("Swim", R.string.swim_emoji); // 🏊
        activityEmojisMap.put("WeightTraining", R.string.weight_training_emoji); // 🏋
        activityEmojisMap.put("RestDay", R.string.rest_day_emoji); // 🏖
    }

    public static String getActivityEmoji(Context context, String activityType) {
        int emojiResId = activityEmojisMap.getOrDefault(activityType, R.string.empty_training);
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

}
