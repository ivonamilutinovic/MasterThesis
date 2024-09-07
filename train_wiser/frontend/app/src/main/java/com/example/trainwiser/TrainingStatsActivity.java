package com.example.trainwiser;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIRetrofitClient;
import com.example.trainwiser.network.APIInterface;
import com.example.trainwiser.network.api_models.stats.TrainingStatsResponseData;
import com.example.trainwiser.network.utils.APIUtils;

import org.json.JSONObject;

import java.net.HttpURLConnection;
import java.util.Calendar;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class TrainingStatsActivity extends AppCompatActivity {
    private Spinner spinnerYear, spinnerMonth;
    private TextView textView;
    private int selectedYear, selectedMonth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_training_stats);
    }

    @Override
    protected void onResume() {
        super.onResume();
        textView = findViewById(R.id.textView);
        spinnerYear = findViewById(R.id.spinner_year);
        spinnerMonth = findViewById(R.id.spinner_month);

        setupSpinners();
    }
    
    private void setupSpinners() {
        // Set up the year spinner
        int currentYear = Calendar.getInstance().get(Calendar.YEAR);
        Integer[] years = new Integer[7];
        for (int i = 0; i < 7; i++) {
            years[i] = currentYear - (6 - i);
        }

        ArrayAdapter<Integer> yearAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, years);
        yearAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerYear.setAdapter(yearAdapter);
        spinnerYear.setSelection(yearAdapter.getPosition(currentYear));

        spinnerYear.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                selectedYear = (int) parent.getItemAtPosition(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                // Do nothing
            }
        });

        // Set up the month spinner
        String[] months = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
        ArrayAdapter<String> monthAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, months);
        monthAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerMonth.setAdapter(monthAdapter);

        spinnerMonth.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                selectedMonth = position + 1; // months are 1-based in the API
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                // Do nothing
            }
        });
    }

    public void getStatisticsRequest(){
        String authHeader = APIUtils.getAuthorizationHeader(TrainingStatsActivity.this);
        APIRetrofitClient.getAPIClient()
                .create(APIInterface.class)
                .getMonthlyStats(authHeader, selectedYear, selectedMonth).enqueue(new Callback<TrainingStatsResponseData>() {
                    @Override
                    public void onResponse(Call<TrainingStatsResponseData> call, Response<TrainingStatsResponseData> response) {
                        if (response.code() == HttpURLConnection.HTTP_OK) {
                            if (response.body() != null) {
                                TrainingStatsResponseData trainingSummary = response.body();
                                displayData(trainingSummary);
                            } else {
                                Toast.makeText(TrainingStatsActivity.this, "Empty response", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            Utils.onResponseErrorLogging(TrainingStatsActivity.this, response);
                        }
                    }

                    @Override
                    public void onFailure(Call<TrainingStatsResponseData> call, Throwable t) {
                        Utils.onFailureLogging(TrainingStatsActivity.this, t);
                    }

                });
    }
    public void getStatistics(View view) {
        APIUtils.refreshAccessTokenIfNeeded(TrainingStatsActivity.this,  new Runnable() {
            @Override
            public void run() {
                getStatisticsRequest();
            }
        });
    }

    private void displayData(TrainingStatsResponseData trainingSummary) {
        StringBuilder sb = new StringBuilder();

        for (String week : trainingSummary.trainingWeeks.keySet()) {
            sb.append("Week: ").append(week).append("\n");
            TrainingStatsResponseData.WeekSummary weekSummary = trainingSummary.trainingWeeks.get(week);

            sb.append("Activities:\n");
            for (TrainingStatsResponseData.Activity activity : weekSummary.activities) {
                String activityEmoji = Utils.getActivityEmoji(getApplicationContext(), activity.activityType);
                if (!activity.activityType.equals("WeightTraining")){
                    sb.append("Date ").append(activity.startDate).append(": ")
                            .append(activityEmoji).append(" ")
                            .append(activity.distance).append("km, ")
                            .append(Utils.secondsInFormatedTime(activity.duration)).append(", ")
                            .append("Z").append(activity.averageHeartrateZone).append("\n");
                }else{
                    sb.append("Date ").append(activity.startDate).append(": ")
                            .append(activityEmoji).append(" ")
                            .append(Utils.secondsInFormatedTime(activity.duration)).append(", ")
                            .append("Z").append(activity.averageHeartrateZone).append("\n");
                }
            }

            sb.append("\nSummary:\n");
            for (String activityType : weekSummary.summary.keySet()) {
                TrainingStatsResponseData.ActivitySummary summary = weekSummary.summary.get(activityType);
                String totalDistance;

                if (activityType.equals("WeightTraining")){
                    totalDistance = "";
                }else{
                    totalDistance = "   • Total Distance: " + summary.totalDistance + "km\n";
                }
                sb.append(activityType).append(":\n")
                        .append("   • Total Duration: ").append(Utils.secondsInFormatedTime(summary.totalDuration)).append("\n")
                        .append(totalDistance)
                        .append("   • Avg HR Zone: Z").append(summary.averageHeartrateZone).append("\n");
            }
            sb.append("\n\n");
        }

        textView.setText(sb.toString());
    }

}