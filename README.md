SMS Reminder - Python, Google Cloud and Twilio

This freelance project was developed for a self-employed entrepreneur in the health services industry. The client faced challenges in consistently sending appointment reminders and obtaining confirmation from customers. Without a proper reminder system, she was unable to enforce her 48-hour cancellation policy.

To address this issue, a solution was designed to automatically send daily reminders at 9:00 a.m. for appointments scheduled within the next 48 hours. The system integrates with Google Calendar, which the client uses to manage her schedule. Additionally, it uses Twilio to send messages and is hosted on Google Cloud.

**Features**
 - Integrates with Google Calendar to fetch scheduled appointments.
 - Send reminders for appointments within the next 48 hours.
 - Send SMS notifications using Twilio.
 - Fully serverless and hosted on Google Cloud Functions (Gen 2).
 - Secure credential management using Secret Manager.
 - Automated daily execution via Cloud Scheduler.

**Tech Stack**
- Python 3.11.
- Google Cloud Functions (Gen 2).
- Google Calendar API.
- Twilio API.
- Google Cloud Scheduler.
- Google Cloud Secret Manager.
  
**How It Works**
- The scheduler triggers the cloud function daily at 9:00 AM (Melbourne time).
- The function retrieves upcoming events from Google Calendar.
- It filters appointments occurring within the next 48 hours.
- For each appointment:
    Extracts event details (date, time, location).
    Read the client’s phone number from the event description.
- Send an SMS reminder using Twilio.

**Implementation**
1. Create your Google Cloud Project.
2. Enable APIs: Google Calendar API, Cloud Functions API, Cloud Scheduler API, Secret Manager API.
3. Create Service Account:
      - Go to IAM / Service Accounts.
      - Create new Service Account.
      - Download JSON Key.
4. Open your Google Calendar and share the calendar with the service account email.
5. Get Account SID, Auth Token and Phone Number from Twilio.
6. Use Google Cloud Secret Manager to store:
      - TWILIO_ACCOUNT_SID
      - TWILIO_AUTH_TOKEN
      - TWILIO_PHONE_NUMBER
      - SERVICE_ACCOUNT_FILE (JSON Key)
7. Add IAM Policy (Secret Manager Secret Accessor) to you project.
8. Create main.py
9. Create requirements.txt
10. Deploy function (gen2)
11. Automate with scheduler

