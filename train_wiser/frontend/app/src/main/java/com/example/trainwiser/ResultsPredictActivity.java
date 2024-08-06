package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import com.example.trainwiser.common.PreferenceType;
import com.example.trainwiser.common.SharedPreferenceSingleton;
import com.example.trainwiser.network.APIClientWithInterceptorForTokens;
import com.example.trainwiser.network.APIInterfaceWithInterceptorForTokens;
import com.example.trainwiser.network.Oauth2Interface;
import com.example.trainwiser.network.Oauth2RetrofitClient;
import com.example.trainwiser.network.api_models.account.AccountDataResponse;
import com.example.trainwiser.network.api_models.login.LoginResponseData;
import com.example.trainwiser.network.api_models.results_prediction.ResultsPredictionRequestData;
import com.example.trainwiser.network.api_models.results_prediction.ResultsPredictionResponseData;
import com.example.trainwiser.network.utils.APIKeys;

import org.json.JSONObject;

import java.net.HttpURLConnection;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ResultsPredictActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_results_prediction);

        Spinner distanceSpinner = findViewById(R.id.distance_spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.race_distances, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        distanceSpinner.setAdapter(adapter);
        distanceSpinner.setSelection(0);
    }

    @Override
    protected void onResume() {
        super.onResume();
        Spinner distanceSpinner = findViewById(R.id.distance_spinner);
        TextView predictedTime = findViewById(R.id.predicted_time);
        distanceSpinner.setSelection(0);
        predictedTime.setText("");
    }

    private int getIndex(Spinner spinner, String value) {
        for (int i = 0; i < spinner.getCount(); i++) {
            if (spinner.getItemAtPosition(i).toString().equalsIgnoreCase(value)) {
                return i;
            }
        }
        return 0;
    }

    public void onClickPredict(View view) {
        Spinner distanceSpinner = findViewById(R.id.distance_spinner);
        String selectedDistance = distanceSpinner.getSelectedItem().toString();
        predictRaceTime(selectedDistance);
    }

    private void predictRaceTime(String distance) {
        float distanceInKm = convertDistanceToFloat(distance);
        ResultsPredictionRequestData resultPredictionData = new ResultsPredictionRequestData(distanceInKm);

        APIClientWithInterceptorForTokens.getAPIClient(ResultsPredictActivity.this)
                .create(APIInterfaceWithInterceptorForTokens.class)
                .getResultsPrediction(resultPredictionData).enqueue(new Callback<ResultsPredictionResponseData>() {
                    @Override
                    public void onResponse(Call<ResultsPredictionResponseData> call, Response<ResultsPredictionResponseData> response) {
                        if (response.code() == HttpURLConnection.HTTP_OK) {
                            if (response.body() != null) {
                                TextView predictedTime = findViewById(R.id.predicted_time);

                                String predictedTimeText = response.body().getRace_result();
                                predictedTime.setText(predictedTimeText);
                            } else {
                                Toast.makeText(ResultsPredictActivity.this, "Empty response", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            ResponseBody errorBody = response.errorBody();
                            String errorText = "Unknown error";
                            if (errorBody != null) {
                                try {
                                    String errorBodyStr = errorBody.string();
                                    JSONObject errorBodyJson = new JSONObject(errorBodyStr);

                                    errorText = errorBodyJson.optString("error", errorText);
                                } catch (Exception ignored) {

                                }
                            }

                            Toast.makeText(ResultsPredictActivity.this,
                                    "Error code: " + response.code() + " (" + errorText + ")", Toast.LENGTH_LONG).show();
                        }}

                    @Override
                    public void onFailure(Call<ResultsPredictionResponseData> call, Throwable t) {

                    }

                });
    }

    private float convertDistanceToFloat(String distance) {
        String distanceWithoutK = distance.replace("k", "");
        return Float.parseFloat(distanceWithoutK);
    }
}