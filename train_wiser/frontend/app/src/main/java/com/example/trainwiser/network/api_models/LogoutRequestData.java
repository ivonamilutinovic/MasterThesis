package com.example.trainwiser.network.api_models;

public class LogoutRequestData {
    private final String client_id;
    private final String client_secret;
    private final String token;

    public LogoutRequestData(String client_id, String client_secret, String token) {
        this.client_id = client_id;
        this.client_secret = client_secret;
        this.token = token;
    }

    public String getClient_id() {
        return client_id;
    }

    public String getClient_secret() {
        return client_secret;
    }

    public String getToken() {
        return token;
    }
}
