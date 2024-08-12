package com.example.trainwiser;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Spinner;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIClientWithInterceptorForTokens;
import com.example.trainwiser.network.APIInterfaceWithInterceptorForTokens;
import com.example.trainwiser.network.api_models.trainings.TrainingPlanResponse;

import org.json.JSONObject;

import java.net.HttpURLConnection;
import java.util.Calendar;
import java.util.List;
import java.util.Map;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class TrainingsSuggestionsActivity extends AppCompatActivity {
    private Spinner distanceSpinner;
    private EditText editTextGoalTime;
    private TableLayout tableTrainings;
    LinearLayout buttonContainer;
    HorizontalScrollView buttonScrollView;
    HorizontalScrollView tableScrollView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trainings_suggestions);

        distanceSpinner = findViewById(R.id.distance_spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.race_distances, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        distanceSpinner.setAdapter(adapter);
        distanceSpinner.setSelection(0);


        editTextGoalTime = findViewById(R.id.editText_goal_time);
        tableTrainings = findViewById(R.id.tableTrainings);
        editTextGoalTime.addTextChangedListener(new TextWatcher() {
            private String current = "";
            private String hhmmss = "HHMMSS";
            private final int[] selection = {2, 5, 8};

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {}

            @Override
            public void afterTextChanged(Editable s) {
                if (!s.toString().equals(current)) {
                    String clean = s.toString().replaceAll("[^\\d]", "");
                    String cleanC = current.replaceAll("[^\\d]", "");

                    int cl = clean.length();
                    int sel = cl;
                    for (int i : selection) {
                        if (cl <= i) break;
                        sel++;
                    }

                    if (clean.equals(cleanC)) sel--;

                    if (clean.length() < 6) {
                        clean = clean + hhmmss.substring(clean.length());
                    } else {
                        clean = clean.substring(0, 6);
                    }

                    clean = String.format("%s:%s:%s",
                            clean.substring(0, 2),
                            clean.substring(2, 4),
                            clean.substring(4, 6));

                    sel = Math.max(sel, 0);
                    current = clean;
                    editTextGoalTime.setText(current);
                    editTextGoalTime.setSelection(Math.min(sel, current.length()));
                }
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        distanceSpinner.setSelection(0);
        editTextGoalTime.setText("");
        editTextGoalTime.setText("");
    }


    public void onClickTrainingSuggestions(View view) {
        String raceDistanceStr = distanceSpinner.getSelectedItem().toString().replace("k", "");;
        String goalTimeStr = editTextGoalTime.getText().toString();

        if (raceDistanceStr.isEmpty() || goalTimeStr.length() != 8) {
            Toast.makeText(this, "Please enter valid values", Toast.LENGTH_SHORT).show();
            return;
        }

        float raceDistance = Float.parseFloat(raceDistanceStr);

        int hours = Integer.parseInt(goalTimeStr.substring(0, 2));
        int minutes = Integer.parseInt(goalTimeStr.substring(3, 5));
        int seconds = Integer.parseInt(goalTimeStr.substring(6, 8));
        int goalTime = hours * 3600 + minutes * 60 + seconds;


        APIClientWithInterceptorForTokens.getAPIClient(TrainingsSuggestionsActivity.this)
                .create(APIInterfaceWithInterceptorForTokens.class)
                .getTrainingPlan(goalTime, raceDistance).enqueue(new Callback<Map<String, List<List<List<TrainingPlanResponse>>>>>() {
                    @Override
                    public void onResponse(Call<Map<String, List<List<List<TrainingPlanResponse>>>>> call, Response<Map<String, List<List<List<TrainingPlanResponse>>>>> response) {
                        if (response.code() == HttpURLConnection.HTTP_OK) {
                            if (response.body() != null) {
                                Map<String, List<List<List<TrainingPlanResponse>>>> trainingPlans = response.body();
                                setRaceResultsButtons(trainingPlans);
                            } else {
                                Toast.makeText(TrainingsSuggestionsActivity.this, "Empty response", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            Utils.onResponseErrorLogging(TrainingsSuggestionsActivity.this, response);
                        }
                    }

                    @Override
                    public void onFailure(Call<Map<String, List<List<List<TrainingPlanResponse>>>>> call, Throwable t) {
                        Utils.onFailureLogging(TrainingsSuggestionsActivity.this, t);
                    }
                });
    }


    private void setRaceResultsButtons(Map<String, List<List<List<TrainingPlanResponse>>>> trainingPlans) {
        LinearLayout buttonContainer = findViewById(R.id.buttonContainer);
        ScrollView buttonScrollView = findViewById(R.id.buttonScrollView);
        HorizontalScrollView tableScrollView = findViewById(R.id.tableScrollView);
        LayoutInflater inflater = LayoutInflater.from(this);
        tableTrainings.removeAllViews();

        for (String key : trainingPlans.keySet()) {
            Button button = (Button) inflater.inflate(R.layout.training_plan_button, buttonContainer, false);
            button.setText(key);

            button.setOnClickListener(v -> {
                buttonScrollView.setVisibility(View.GONE);
                tableScrollView.setVisibility(View.VISIBLE);

                List<List<List<TrainingPlanResponse>>> trainingPlan = trainingPlans.get(key);
                displayTrainingSuggestions(trainingPlan);
            });

            buttonContainer.addView(button);
        }
    }

    private void displayTrainingSuggestions(List<List<List<TrainingPlanResponse>>> trainingSuggestions) {
        String activityEmoji;

        tableTrainings.removeAllViews();

        TableRow headerRow = new TableRow(this);
        TextView headerWeeks = createTextView("Weeks\\Days", true);
        headerRow.addView(headerWeeks);

        for (int i = 1; i <= 7; i++) {
            TextView headerDay = createTextView("Day " + i, true);
            headerRow.addView(headerDay);
        }
        tableTrainings.addView(headerRow);

        for (int weekIndex = 0; weekIndex < trainingSuggestions.size(); weekIndex++) {
            TableRow weekRow = new TableRow(this);

            TextView weekLabel = createTextView("Week " + (weekIndex + 1), true);
            weekRow.addView(weekLabel);
            weekLabel.setHeight(200);
            List<List<TrainingPlanResponse>> week = trainingSuggestions.get(weekIndex);
            for (List<TrainingPlanResponse> day : week) {
                TextView dayLabel = createTextView("", false);
                dayLabel.setHeight(200);
                if (day.size() == 1 && day.get(0).getActivityType().equals("RestDay")) {
                    activityEmoji = Utils.getActivityEmoji(getApplicationContext(), "RestDay");
                    dayLabel.setText(activityEmoji);
                } else {
                    StringBuilder dayText = new StringBuilder();
                    for (TrainingPlanResponse training : day) {
                        activityEmoji = Utils.getActivityEmoji(getApplicationContext(), training.getActivityType());
                        String distance;

                        if (training.getActivityType().equals("WeightTraining")){
                            distance = "";
                        }else{
                            distance = training.getDistance() + "km, ";
                        }

                        dayText.append(activityEmoji)
                                .append(distance)
                                .append(Utils.secondsInFormatedTime(training.getDuration()))
                                .append(", Z").append(training.getAverageHeartrateZone())
                                .append("\n");
                    }
                    dayLabel.setText(dayText.toString().trim());
                }
                weekRow.addView(dayLabel);
            }

            tableTrainings.addView(weekRow);
        }
    }

    private TextView createTextView(String text, boolean isHeader) {
        TextView textView = new TextView(this);
        textView.setText(text);
        textView.setPadding(8, 8, 8, 8);
        textView.setBackgroundResource(R.drawable.table_border);
        if (isHeader) {
            textView.setTypeface(null, android.graphics.Typeface.BOLD);
        }
        return textView;
    }
}

