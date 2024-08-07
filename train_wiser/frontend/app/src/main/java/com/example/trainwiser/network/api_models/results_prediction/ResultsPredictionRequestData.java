package com.example.trainwiser.network.api_models.results_prediction;

public class ResultsPredictionRequestData {
    private final String race_distance;

    public ResultsPredictionRequestData(String race_distance) {
        this.race_distance = race_distance;
    }

    public String getRace_distance() {
        return race_distance;
    }

}
