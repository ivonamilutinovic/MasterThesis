package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import com.example.trainwiser.network.APIClientWithInterceptorForTokens;
import com.example.trainwiser.network.APIInterfaceWithInterceptorForTokens;
import com.example.trainwiser.network.api_models.stats.TrainingStatsResponseData;

import org.json.JSONObject;

import java.net.HttpURLConnection;
import java.util.Calendar;
import java.util.Locale;

public class TrainingStatsActivity extends AppCompatActivity {
    private Spinner spinnerYear, spinnerMonth;
    private Button buttonGetStatistics;
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
        buttonGetStatistics = findViewById(R.id.button_get_statistics);

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

        // Set the default selected year to the current year
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

    public void getStatistics(View view) {
        APIClientWithInterceptorForTokens.getAPIClient(TrainingStatsActivity.this)
                .create(APIInterfaceWithInterceptorForTokens.class)
                .getMonthlyStats(selectedYear, selectedMonth).enqueue(new Callback<TrainingStatsResponseData>() {
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

                            Toast.makeText(TrainingStatsActivity.this,
                                    "Error code: " + response.code() + " (" + errorText + ")", Toast.LENGTH_LONG).show();
                        }}

                    @Override
                    public void onFailure(Call<TrainingStatsResponseData> call, Throwable t) {
                        int a = 1;

                    }

                });
    }

    // todo: add constraint that this is possible only for strava users
    private void displayData(TrainingStatsResponseData trainingSummary) {
        StringBuilder sb = new StringBuilder();

        for (String week : trainingSummary.trainingWeeks.keySet()) {
            sb.append("Week: ").append(week).append("\n");
            TrainingStatsResponseData.WeekSummary weekSummary = trainingSummary.trainingWeeks.get(week);

            sb.append("Activities:\n");
            for (TrainingStatsResponseData.Activity activity : weekSummary.activities) {
                if (!activity.activityType.equals("WeightTraining")){
                    sb.append(activity.activityType).append(": ")
                            .append("Distance: ").append(activity.distance).append(" km, ")
                            .append("Duration: ").append(formatDuration(activity.duration)).append(" , ")
                            .append("Avg HR Zone: ").append(activity.averageHeartrateZone).append("\n");
                }else{
                    sb.append(activity.activityType).append(": ")
                            .append("Duration: ").append(formatDuration(activity.duration)).append(" , ")
                            .append("Avg HR Zone: ").append(activity.averageHeartrateZone).append("\n");
                }
            }

            sb.append("Summary:\n");
            for (String activityType : weekSummary.summary.keySet()) {
                TrainingStatsResponseData.ActivitySummary summary = weekSummary.summary.get(activityType);
                sb.append(activityType).append(": ")
                        .append("Total Duration: ").append(formatDuration(summary.totalDuration)).append(" , ")
                        .append("Total Distance: ").append(summary.totalDistance).append(" km, ")
                        .append("Avg HR Zone: ").append(summary.averageHeartrateZone).append("\n");
            }
            sb.append("\n");
        }

        textView.setText(sb.toString());
    }

    private static String formatDuration(Integer seconds) {
        if (seconds == null)
            return "00:00:00";

        int hours = seconds / 3600;
        int remainder = seconds % 3600;
        int minutes = remainder / 60;
        seconds = remainder % 60;

        return String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds);
    }
}