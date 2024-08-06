package com.example.trainwiser.network.api_models.results_prediction;

public class ResultsPredictionResponseData {
    private String race_result;

    public ResultsPredictionResponseData(String race_result) {
        this.race_result = race_result;
    }

    public String getRace_result() {
        return race_result;
    }

    public void setRace_result(String race_result) {
        this.race_result = race_result;
    }
}
