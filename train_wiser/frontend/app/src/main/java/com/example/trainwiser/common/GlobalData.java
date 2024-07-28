package com.example.trainwiser.common;

public class GlobalData {
    private final static String backendUrl = "https://feasible-brightly-cobra.ngrok-free.app/";
    private final static String clientSecret = "LI10Y8vRDXbm3lKpbU5Ugg2Uqj9cLTfObBGqrrMDOsgbtrFii6kqPuTu90HQAkvAU9aKHRvKnjPuPvjr2GVJPjKAX6SHsnoxYlWu6iSWBFA7GVFWCGjGxHMcEqUOfjKh";
    private final static String clientId = "0gPJ2pEgrFTUaFp6h1qqOxjX0S5Q9XsUO9OjySQ1";

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
