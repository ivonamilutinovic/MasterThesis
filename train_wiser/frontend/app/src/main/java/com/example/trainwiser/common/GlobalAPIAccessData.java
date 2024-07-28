package com.example.trainwiser.common;

public class GlobalAPIAccessData {
    private final static String backendUrl = "https://feasible-brightly-cobra.ngrok-free.app/";
    private final static String clientSecret = "LI10Y8vRDXbm3lKpbU5Ugg2Uqj9cLTfObBGqrrMDOsgbtrFii6kqPuTu90HQAkvAU9aKHRvKnjPuPvjr2GVJPjKAX6SHsnoxYlWu6iSWBFA7GVFWCGjGxHMcEqUOfjKh";
    private final static String clientId = "0gPJ2pEgrFTUaFp6h1qqOxjX0S5Q9XsUO9OjySQ1";
    private final static String stravaClientId = "121978";
    private static String stravaAuthorizationURL = null;

    private static String stravaDeauthorizationURL = null;

    public static String getBackendUrl() {
        return backendUrl;
    }

    public static String getClientSecret() {
        return clientSecret;
    }

    public static String getClientId() {
        return clientId;
    }

    public static String getStravaAuthorizationURL() {
        Integer strava_athlete_id = (Integer) APIReceivedDataSingleton.getInstance().getObject("strava_athlete_id");
        if (strava_athlete_id != null) {
            stravaAuthorizationURL = "https://www.strava.com/api/v3/oauth/authorize?" +
                    "response_type=code&" +
                    "client_id=" + stravaClientId + "&" +
                    "scope=profile%3Aread_all,activity%3Aread_all,read&" +
                    "redirect_uri=" + backendUrl + "strava_gateway/token_exchange";
        }
        return stravaAuthorizationURL;
    }

    public static String getStravaDeauthorizationURL() {
        Integer strava_athlete_id = (Integer) APIReceivedDataSingleton.getInstance().getObject("strava_athlete_id");
        if (strava_athlete_id != null) {
            String access_token = "";
            stravaDeauthorizationURL = "https://www.strava.com/api/v3/oauth/deauthorize" +
                    "?access_token=" + access_token;
        }
        return stravaDeauthorizationURL;
    }
}
