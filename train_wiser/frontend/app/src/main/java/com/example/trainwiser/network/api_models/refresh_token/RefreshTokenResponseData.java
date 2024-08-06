package com.example.trainwiser.network.api_models.refresh_token;

import com.google.gson.annotations.SerializedName;
public class RefreshTokenResponseData {

    @SerializedName("access_token")
    private String accessToken;

    @SerializedName("expires_in")
    private int expiresIn;

    public String getAccessToken() {
        return accessToken;
    }

    public int getExpiresIn() {
        return expiresIn;
    }

}
