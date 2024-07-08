package com.example.trainwiser.network;

import android.content.Context;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class APIUtils {

//    public static boolean GetAccessToken(Context ctx, String email, String password) {
//        Map<String, String> headers = new HashMap<>();
//
//        JSONObject requestData = new JSONObject();
//
//        try {
//            requestData.put("username", email);
//            requestData.put("password", password);
//            requestData.put("grant_type", "password");
//            requestData.put("client_id", GlobalVars.GetApiClientId());
//            requestData.put("client_secret", GlobalVars.GetApiClientSecret());
//        } catch (JSONException e) {
//            return false;
//        }
//
//        return SendRequest(ctx, "POST", "/o/token", headers, requestData, handler);
//    }
//
//    public static boolean RefreshAccessToken(Context ctx, String email, String password) {
//        Map<String, String> headers = new HashMap<>();
//
//        JSONObject requestData = new JSONObject();
//
//        try {
//            requestData.put("refresh_token", refresh_token);
//            requestData.put("grant_type", "refresh_token");
//            requestData.put("client_id", GlobalVars.GetApiClientId());
//            requestData.put("client_secret", GlobalVars.GetApiClientSecret());
//        } catch (JSONException e) {
//            return false;
//        }
//
//        return SendRequest(ctx, "POST", "/o/token", headers, requestData, handler);
//    }
}
