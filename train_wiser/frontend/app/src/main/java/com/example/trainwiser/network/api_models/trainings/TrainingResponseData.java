package com.example.trainwiser.network.api_models.trainings;

import com.google.gson.annotations.SerializedName;

public class TrainingResponseData {
    @SerializedName("activity_type")
    private String activityType;

    @SerializedName("distance")
    private float distance;

    @SerializedName("duration")
    private int duration;

    @SerializedName("average_heartrate_zone")
    private int averageHeartrateZone;

    // Getters and Setters
    public String getActivityType() {
        return activityType;
    }

    public void setActivityType(String activityType) {
        this.activityType = activityType;
    }

    public float getDistance() {
        return distance;
    }

    public void setDistance(float distance) {
        this.distance = distance;
    }

    public int getDuration() {
        return duration;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public int getAverageHeartrateZone() {
        return averageHeartrateZone;
    }

    public void setAverageHeartrateZone(int averageHeartrateZone) {
        this.averageHeartrateZone = averageHeartrateZone;
    }
}
