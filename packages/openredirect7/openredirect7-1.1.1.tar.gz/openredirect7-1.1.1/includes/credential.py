from twilio.rest import Client

TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_WHATSAPP = ""
TWILIO_TO_WHATSAPP = ""

def send_whatsapp_message(message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_FROM_WHATSAPP}',
            to=f'whatsapp:{TWILIO_TO_WHATSAPP}'
        )
        print(f"Message SID: {message.sid}")
        print(f"Message Status: {message.status}")
    except Exception as e:
        print(f"Failed to send message: {e}")
