package com.example.trainwiser.common;

import java.util.HashMap;

public class APIReceivedDataSingleton {
    private static APIReceivedDataSingleton instance;
    HashMap<String, Object> apiDataMap = new HashMap<>();

    private APIReceivedDataSingleton() {
    }

    public static synchronized APIReceivedDataSingleton getInstance() {
        if (instance == null)
            instance = new APIReceivedDataSingleton();

        return instance;
    }

    public HashMap<String, Object> getApiDataMap() {
        return apiDataMap;
    }

    public void addObject(String key, Object entry) {
        apiDataMap.put(key, entry);
    }

    public Object getObject(String key) {
        return apiDataMap.get(key);
    }
}
