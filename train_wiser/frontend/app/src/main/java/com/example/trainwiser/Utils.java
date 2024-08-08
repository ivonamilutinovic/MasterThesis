package com.example.trainwiser;

import java.util.HashMap;
import java.util.Map;

public class Utils {
    public static final Map<String, String> activityEmojisMap = new HashMap<>();

    static {
        activityEmojisMap.put("Run", "\uD83C\uDFC3"); // 🏃
        activityEmojisMap.put("Ride", "\uD83D\uDEB2"); // 🚲
        activityEmojisMap.put("Swim", "\uD83C\uDFCA"); // 🏊
        activityEmojisMap.put("WeightTraining", "\uD83C\uDFCB"); // 🏋
        activityEmojisMap.put("RestDay", "\uD83C\uDFD6"); // 🏖
    }

}
