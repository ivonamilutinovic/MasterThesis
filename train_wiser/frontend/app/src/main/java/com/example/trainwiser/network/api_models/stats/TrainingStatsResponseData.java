package com.example.trainwiser.network.api_models.stats;

import com.google.gson.annotations.SerializedName;
import java.util.Map;
import java.util.List;

public class TrainingStatsResponseData {
    @SerializedName("training_weeks")
    public Map<String, WeekSummary> trainingWeeks;

    public static class WeekSummary {
        @SerializedName("activities")
        public List<Activity> activities;

        @SerializedName("summary")
        public Map<String, ActivitySummary> summary;
    }

    public static class Activity {
        @SerializedName("activity_type")
        public String activityType;

        @SerializedName("distance")
        public float distance;

        @SerializedName("duration")
        public int duration;

        @SerializedName("average_heartrate_zone")
        public int averageHeartrateZone;
    }

    public static class ActivitySummary {
        @SerializedName("total_duration")
        public int totalDuration;

        @SerializedName("total_distance")
        public float totalDistance;

        @SerializedName("average_heartrate_zone")
        public int averageHeartrateZone;
    }

    public TrainingStatsResponseData(Map<String, WeekSummary> trainingWeeks) {
        this.trainingWeeks = trainingWeeks;
    }

    public Map<String, WeekSummary> getTrainingWeeks() {
        return trainingWeeks;
    }

    public void setTrainingWeeks(Map<String, WeekSummary> trainingWeeks) {
        this.trainingWeeks = trainingWeeks;
    }
}
