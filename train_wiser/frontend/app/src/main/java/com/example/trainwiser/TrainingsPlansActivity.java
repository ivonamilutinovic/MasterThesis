package com.example.trainwiser;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
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

import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIRetrofitClient;
import com.example.trainwiser.network.APIInterface;
import com.example.trainwiser.network.api_models.trainings.TrainingPlanResponse;
import com.example.trainwiser.network.utils.APIUtils;

import java.net.HttpURLConnection;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class TrainingsPlansActivity extends AppCompatActivity {
    private Spinner distanceSpinner;
    private EditText editTextGoalTime;
    private TableLayout tableTrainings;
    private String initialSelectedDistance;
    private String initialGoalTime;
    ScrollView buttonScrollView;
    HorizontalScrollView tableScrollView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_training_plans);

        distanceSpinner = findViewById(R.id.distance_spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.race_distances, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        distanceSpinner.setAdapter(adapter);
        distanceSpinner.setSelection(0);

        editTextGoalTime = findViewById(R.id.editText_goal_time);
        tableTrainings = findViewById(R.id.tableTrainings);
        editTextGoalTime.addTextChangedListener(new TextWatcher() {
            private String previousFormattedTime = "";
            private String hhmmssPlaceholder = "HHMMSS";
            private final int[] selection = {2, 5, 8};

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {}

            @Override
            public void afterTextChanged(Editable s) {
                if (!s.toString().equals(previousFormattedTime)) {
                    String onlyDigitsInput = s.toString().replaceAll("[^\\d]", "");
                    String onlyDigitsPrevious = previousFormattedTime.replaceAll("[^\\d]", "");

                    int inputLength = onlyDigitsInput.length();
                    int cursorPosition = inputLength;
                    for (int selectionIndex : selection) {
                        if (inputLength <= selectionIndex) break;
                        cursorPosition++;
                    }

                    if (onlyDigitsInput.equals(onlyDigitsPrevious)) cursorPosition--;

                    if (onlyDigitsInput.length() < 6) {
                        onlyDigitsInput = onlyDigitsInput + hhmmssPlaceholder.substring(onlyDigitsInput.length());
                    } else {
                        onlyDigitsInput = onlyDigitsInput.substring(0, 6);
                    }

                    onlyDigitsInput = String.format("%s:%s:%s",
                            onlyDigitsInput.substring(0, 2),
                            onlyDigitsInput.substring(2, 4),
                            onlyDigitsInput.substring(4, 6));

                    cursorPosition = Math.max(cursorPosition, 0);
                    previousFormattedTime = onlyDigitsInput;
                    editTextGoalTime.setText(previousFormattedTime);
                    editTextGoalTime.setSelection(Math.min(cursorPosition, previousFormattedTime.length()));
                }
            }

        });
    }

    @Override
    protected void onResume() {
        super.onResume();

        buttonScrollView = findViewById(R.id.buttonScrollView);
        tableScrollView = findViewById(R.id.tableScrollView);
        distanceSpinner.setSelection(0);
        editTextGoalTime.setText("");

        OnBackPressedCallback onBackPressedCallback = new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                if (buttonScrollView.getVisibility() == View.GONE &&
                        tableScrollView.getVisibility() == View.VISIBLE) {
                    buttonScrollView.setVisibility(View.VISIBLE);
                    tableScrollView.setVisibility(View.GONE);
                } else {
                    finish();
                }
            }
        };

        getOnBackPressedDispatcher().addCallback(this, onBackPressedCallback);
    }


    public void onClickTrainingSuggestions(View view) {
        String raceDistanceStr = distanceSpinner.getSelectedItem().toString().replace("k", "");;
        String goalTimeStr = editTextGoalTime.getText().toString();

        String currentSelectedDistance = distanceSpinner.getSelectedItem().toString();
        String currentGoalTime = editTextGoalTime.getText().toString();
        if (currentSelectedDistance.equals(initialSelectedDistance) && currentGoalTime.equals(initialGoalTime)) {
            return;
        }
        initialSelectedDistance = distanceSpinner.getSelectedItem().toString();
        initialGoalTime = editTextGoalTime.getText().toString();

        if (raceDistanceStr.isEmpty() || goalTimeStr.length() != 8) {
            Toast.makeText(this, "Please enter valid values", Toast.LENGTH_LONG).show();
            return;
        }

        float raceDistance = Float.parseFloat(raceDistanceStr);

        int hours = Integer.parseInt(goalTimeStr.substring(0, 2));
        int minutes = Integer.parseInt(goalTimeStr.substring(3, 5));
        int seconds = Integer.parseInt(goalTimeStr.substring(6, 8));

        if (hours > 24) {
            Toast.makeText(TrainingsPlansActivity.this, "Hours must be less than or equal to 24", Toast.LENGTH_LONG).show();
            editTextGoalTime.setText("");
            return;
        }

        if (minutes > 59) {
            Toast.makeText(TrainingsPlansActivity.this, "Minutes must be less than or equal to 59", Toast.LENGTH_LONG).show();
            editTextGoalTime.setText("");
            return;
        }

        if (seconds > 59) {
            Toast.makeText(TrainingsPlansActivity.this, "Seconds must be less than or equal to 59", Toast.LENGTH_LONG).show();
            editTextGoalTime.setText("");
            return;
        }

        int goalTime = hours * 3600 + minutes * 60 + seconds;

        APIUtils.refreshAccessTokenIfNeeded(TrainingsPlansActivity.this,  new Runnable() {
            @Override
            public void run() {
                getTrainingPlansRequest(goalTime, raceDistance);
            }
        });
    }

    public void getTrainingPlansRequest(int goalTime, float raceDistance){
        String authHeader = APIUtils.getAuthorizationHeader(TrainingsPlansActivity.this);
        APIRetrofitClient.getAPIClient()
                .create(APIInterface.class)
                .getTrainingPlan(authHeader, goalTime, raceDistance).enqueue(new Callback<Map<String, List<List<List<TrainingPlanResponse>>>>>() {
                    @Override
                    public void onResponse(Call<Map<String, List<List<List<TrainingPlanResponse>>>>> call, Response<Map<String, List<List<List<TrainingPlanResponse>>>>> response) {
                        if (response.code() == HttpURLConnection.HTTP_OK) {
                            if (response.body() != null) {
                                Map<String, List<List<List<TrainingPlanResponse>>>> trainingPlans = response.body();
                                setRaceResultsButtons(trainingPlans);
                            } else {
                                Toast.makeText(TrainingsPlansActivity.this, "There are no available trainings for specified distance", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            Utils.onResponseErrorLogging(TrainingsPlansActivity.this, response);
                        }
                    }

                    @Override
                    public void onFailure(Call<Map<String, List<List<List<TrainingPlanResponse>>>>> call, Throwable t) {
                        Utils.onFailureLogging(TrainingsPlansActivity.this, t);
                    }
                });
    }


    private void setRaceResultsButtons(Map<String, List<List<List<TrainingPlanResponse>>>> trainingPlans) {
        LinearLayout buttonContainer = findViewById(R.id.buttonContainer);
        buttonScrollView = findViewById(R.id.buttonScrollView);
        tableScrollView = findViewById(R.id.tableScrollView);
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

