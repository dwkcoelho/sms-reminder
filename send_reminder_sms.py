import json
import functions_framework
import pytz
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import secretmanager
from datetime import datetime, timedelta
from twilio.rest import Client

PROJECT_ID = "sms-reminder-avotherapy"

def access_secret(secret_name):

    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"

    response = client.access_secret_version(request={"name": name})

    return response.payload.data.decode("UTF-8")


@functions_framework.http
def send_reminder_sms(request):
    # Twilio Setup
    ACCOUNT_SID = access_secret("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN  = access_secret("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE = access_secret("TWILIO_PHONE_NUMBER")
    twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Google Calendar Setup
    service_account_json = access_secret("SERVICE_ACCOUNT_FILE")

    credentials_info = json.loads(service_account_json)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )

    service = build('calendar', 'v3', credentials=credentials)

    # Get events from Google Calendar
    now = datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="dwkcoelho@gmail.com",
        timeMin=now,
        maxResults=20,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get("items", [])

    # Filter events for 2 days later
    tz = pytz.timezone('Australia/Melbourne')
    now = datetime.now(tz)
    today = now.date()
    target_date = today + timedelta(days=2)

    for event in events:
        start_event  = event["start"].get("dateTime", event["start"].get("date"))
        start = datetime.fromisoformat(start_event)

        if start.date() == target_date:
            end_event  = event["end"].get("dateTime", event["end"].get("end"))
            end = datetime.fromisoformat(end_event)

            message_body = (
                f"Reminder: {event.get('summary')}\n"
                f"Date: {start.strftime('%d/%m/%Y')}\n"
                f"Time: {start.strftime('%I:%M %p').lstrip('0')} - {end.strftime('%I:%M %p').lstrip('0')}\n"
                f"Location: {event.get('location') or 'Not provided'}"
            )

            # The 'description' field should contain the phone number
            phone_number = event.get("description")
            if phone_number:
                twilio_client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE,
                    to=phone_number
                )

    return {"status": "reminders_sent"}