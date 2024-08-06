package com.example.trainwiser.network.api_models.refresh_token;
import com.google.gson.annotations.SerializedName;

public class RefreshTokenRequestData {
    @SerializedName("grant_type")
    private final String grantType;

    @SerializedName("refresh_token")
    private final String refreshToken;

    @SerializedName("client_id")
    private final String clientId;

    @SerializedName("client_secret")
    private final String clientSecret;

    public RefreshTokenRequestData(String grantType, String refreshToken, String clientId, String clientSecret) {
        this.grantType = grantType;
        this.refreshToken = refreshToken;
        this.clientId = clientId;
        this.clientSecret = clientSecret;
    }

    public String getGrantType() {
        return grantType;
    }

    public String getRefreshToken() {
        return refreshToken;
    }

    public String getClientId() {
        return clientId;
    }

    public String getClientSecret() {
        return clientSecret;
    }
}
