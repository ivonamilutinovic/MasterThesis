package com.example.trainwiser.network.api_models.account;

public class AccountDataResponse {
    private Integer strava_athlete_id;
    private String username;
    private String email;
    private String first_name;
    private String last_name;
    private String password;
    private String birth_date;

    public AccountDataResponse(Integer strava_athlete_id, String username, String email,
                               String first_name, String last_name, String password, String birth_date) {
        this.strava_athlete_id = strava_athlete_id;
        this.username = username;
        this.email = email;
        this.first_name = first_name;
        this.last_name = last_name;
        this.password = password;
        this.birth_date = birth_date;
    }

    public Integer getStrava_athlete_id() {
        return strava_athlete_id;
    }

    public void setStrava_athlete_id(Integer strava_athlete_id) {
        this.strava_athlete_id = strava_athlete_id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirst_name() {
        return first_name;
    }

    public void setFirst_name(String first_name) {
        this.first_name = first_name;
    }

    public String getLast_name() {
        return last_name;
    }

    public void setLast_name(String last_name) {
        this.last_name = last_name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getBirth_date() {
        return birth_date;
    }

    public void setBirth_date(String birth_date) {
        this.birth_date = birth_date;
    }

}
