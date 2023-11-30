# CalendarChecker

This script checks the calendars listed in calendar_ids regularly (`check_interval_min`). The events also get stored in `captured_filename` so that when the script gets restarted continues where it was left.

Credentails (created by ChatGPT)

1. Go to the Google Cloud Console:
- Visit the [Google Cloud Console](https://console.cloud.google.com/).

2. Create or Select a Project:
- If you don't have a project, create a new one. If you have an existing project, select it from the project dropdown.

3. Enable the Google Calendar API:
- In the left-hand navigation pane, click on "APIs & Services" > "Dashboard."
- Click on the "+ ENABLE APIS AND SERVICES" button.
- In the search bar, type "Google Calendar API" and select it from the results.
- Click the "ENABLE" button to enable the API for your project.

4. Create Credentials:
- After enabling the API, you'll need to create credentials to authenticate your application.
- In the left-hand navigation pane, click on "APIs & Services" > "Credentials."
- Click on the "Create Credentials" button and choose "Service account key."
- Fill out the form:
Service account name: Give your service account a name.
Role: Choose "Project" > "Editor" (or a role with the necessary permissions).
Key type: Choose JSON.
- Click the "Create" button. This will download a JSON file containing your credentials. Keep this file secure and don't share it publicly.

5. Use the JSON File in Your Python Script:
- Replace credentials_filename in your Python script with the path to the JSON file you downloaded.
