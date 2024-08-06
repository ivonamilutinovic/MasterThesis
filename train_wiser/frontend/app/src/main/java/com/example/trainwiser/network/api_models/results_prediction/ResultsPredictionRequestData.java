package com.example.trainwiser.network.api_models.results_prediction;

public class ResultsPredictionRequestData {
    private final float race_distance;

    public ResultsPredictionRequestData(float race_distance) {
        this.race_distance = race_distance;
    }

    public float getRace_distance() {
        return race_distance;
    }

}
