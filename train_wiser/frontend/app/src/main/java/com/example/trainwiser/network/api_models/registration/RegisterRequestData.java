package com.example.trainwiser.network.api_models.registration;

public class RegisterRequestData {
    private final String username;
    private final String email;
    private final String first_name;
    private final String last_name;
    private final String password;
    private final String birth_date;

    public RegisterRequestData(String username, String email, String first_name, String last_name, String password, String birth_date) {
        this.username = username;
        this.email = email;
        this.first_name = first_name;
        this.last_name = last_name;
        this.password = password;
        this.birth_date = birth_date;
    }

    public String getUsername() {
        return username;
    }

    public String getEmail() {
        return email;
    }

    public String getFirst_name() {
        return first_name;
    }

    public String getLast_name() {
        return last_name;
    }

    public String getPassword() {
        return password;
    }

    public String getBirth_date() {
        return birth_date;
    }

}
