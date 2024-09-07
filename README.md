# Train Wiser application

The Train Wiser application provides statistics and training assistance to athletes based on user data imported from 
the Strava app via its public API, as well as results from races held in the Republic of Serbia. It offers users the 
ability to create training plans, view monthly training statistics, and predict race outcomes. The app is designed for 
runners who wish to track their performance more closely and improve their results.

The application was developed as a practical component of a master's thesis at the Faculty of Mathematics, University of Belgrade.

## Project Setup

The project consists of two main components - the server-side (Django application) and the client-side (Android application). 
To set up project, follow the steps below.

### Server-Side (Django)

1. Install the required dependencies using the `requirements.txt` file.
   ```
   cd train_wiser/backend/
   pip install -r requirements.txt
   ```

2. Configure Environment Variables

3. Create a .env file on the path `train_wiser/backend/core/.env`. Use the following template to define the necessary variables:

    ```
    SECRET_KEY= # Django secret key
    STRAVA_CLIENT_ID= # Strava Client ID for authentication of Train Wiser application
    STRAVA_CLIENT_SECRET= # Strava Client Secret for authentication of Train Wiser application
    STRAVA_WEBHOOK_ENDPOINT= # Strava webhook endpoint for Train Wiser application
    HOSTNAME= # Train Wiser application hostname 
    ```

    Ensure to replace the placeholders with actual values.

4. Apply Database Migrations

    Once the environment variables are set up and the dependencies are installed, apply the database migrations to create the necessary tables:
    ```
    cd train_wiser/backend/core
    python manage.py migrate 
    ```

    This will apply all the migrations and set up the database for the Django application.


5. For webhook subscription on Strava application, POST request must be sent on `webhook_subscription` rute to trigger webhook creation.

### Client-Side (Android)

To set up the Android client-side application, ensure you have the following installed:

1. Java Development Kit (JDK)

  The application uses OpenJDK version 11. Current version of Java can be checked with the following command:

  ```
  java -version
  ```

2. Android SDK
 
The application uses Android SDK version 34 for compiling the app, with a minimum SDK version 26. 
Ensure that the correct versions is installed by checking SDK settings in the build.gradle file:

  ```
    compileSdk = 34
    minSdk = 26
  ```
