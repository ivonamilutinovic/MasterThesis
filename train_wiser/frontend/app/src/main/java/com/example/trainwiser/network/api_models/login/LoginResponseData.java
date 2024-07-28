package com.example.trainwiser.network.api_models.login;

public class LoginResponseData {
    private final String access_token;
    private final long expires_in;
    private final String token_type;
    private final String scope;
    private final String refresh_token;

    public LoginResponseData(String access_token, long expires_in, String token_type, String scope, String refresh_token) {
        this.access_token = access_token;
        this.expires_in = expires_in;
        this.token_type = token_type;
        this.scope = scope;
        this.refresh_token = refresh_token;
    }

    public String getAccess_token() {
        return access_token;
    }

    public long getExpires_in() {
        return expires_in;
    }

    public String getRefresh_token() {
        return refresh_token;
    }
}
