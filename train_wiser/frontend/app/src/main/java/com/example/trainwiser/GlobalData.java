package com.example.trainwiser;

public class GlobalData {
    private final static String backendUrl = "https://feasible-brightly-cobra.ngrok-free.app/";
    private final static String clientSecret = "";
    private final static String clientId = "";

    public static String getBackendUrl() {
        return backendUrl;
    }

    public static String getClientSecret() {
        return clientSecret;
    }

    public static String getClientId() {
        return clientId;
    }
}
