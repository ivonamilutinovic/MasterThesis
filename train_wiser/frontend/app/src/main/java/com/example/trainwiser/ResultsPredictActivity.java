package com.example.trainwiser;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIRetrofitClient;
import com.example.trainwiser.network.APIInterface;
import com.example.trainwiser.network.api_models.results_prediction.ResultsPredictionResponseData;
import com.example.trainwiser.network.utils.APIUtils;

import org.json.JSONObject;

import java.net.HttpURLConnection;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ResultsPredictActivity extends AppCompatActivity {
    Spinner distanceSpinner;
    TextView predictedTime;
    TextView predictedTimeLabel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_results_prediction);

        distanceSpinner = findViewById(R.id.distance_spinner);
        predictedTime = findViewById(R.id.predicted_time);
        predictedTimeLabel = findViewById(R.id.predicted_label);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.race_distances, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        distanceSpinner.setAdapter(adapter);
        distanceSpinner.setSelection(0);
    }

    @Override
    protected void onResume() {
        super.onResume();
        distanceSpinner.setSelection(0);
        predictedTime.setText("");
        predictedTimeLabel.setText("");
    }

    public void onClickPredict(View view) {
        String selectedDistance = distanceSpinner.getSelectedItem().toString();
        predictRaceTime(selectedDistance);
    }

    private void predictRaceTimeRequest(String distance) {
        String distanceWithoutK = distance.replace("k", "");
        String authHeader = APIUtils.getAuthorizationHeader(ResultsPredictActivity.this);

        APIRetrofitClient.getAPIClient()
                .create(APIInterface.class)
                .getResultsPrediction(authHeader, distanceWithoutK).enqueue(new Callback<ResultsPredictionResponseData>() {
                    @Override
                    public void onResponse(Call<ResultsPredictionResponseData> call, Response<ResultsPredictionResponseData> response) {
                        if (response.code() == HttpURLConnection.HTTP_OK) {
                            if (response.body() != null) {
                                String predictedTimeText = response.body().getRace_result();
                                predictedTime.setText(predictedTimeText);
                                predictedTimeLabel.setText(R.string.predicted_time_according_to_races_in_serbia);
                            } else {
                                Toast.makeText(ResultsPredictActivity.this, "Empty response", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            Utils.onResponseErrorLogging(ResultsPredictActivity.this, response);
                        }

                    }

                    @Override
                    public void onFailure(Call<ResultsPredictionResponseData> call, Throwable t) {
                        Utils.onFailureLogging(ResultsPredictActivity.this, t);
                    }

                });
    }

    private void predictRaceTime(String distance) {

        APIUtils.refreshAccessTokenIfNeeded(ResultsPredictActivity.this,  new Runnable() {
            @Override
            public void run() {
                predictRaceTimeRequest(distance);
            }
        });

    }
}