import os
import time
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# 1. Initialize the Twilio Client with your single Account SID and Auth Token
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'ENTER_CODE')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'ENTER_CODE')
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# 2. Define your pool of Twilio outbound numbers
twilio_caller_ids = [
    '+YOUR_numbers', 
    '+YOUR_numbers', 
    '+YOUR_numbers'
]

# 3. Define the list of recipients you want to call
target_recipients = [
    '+1717876scammer',
    '+1717876scammer',
    '+1717876scammer',
    '+1717876scammer',
    '+1717876scammer',
    '+1717876scammer',
    '+1717876scammer',
    '+1717876scammer',
    '+1717876scammer',
    '+ETC ETC ETC',
    '+1717876scammer'	
]

# 4. Your audio instructions: Be creative :)
audio_url = 'https://url_to_your_hosted_file/stop.mp3' 
twiml_url = f'https://twimlets.com/echo?Twiml=%3CResponse%3E%3CPlay%3E{audio_url}%3C%2FPlay%3E%3C%2FResponse%3E'

print(f"Starting broadcast to {len(target_recipients)} numbers using {len(twilio_caller_ids)} outbound lines...\n")

# 5. Loop through recipients and rotate the outbound numbers
for index, target_number in enumerate(target_recipients):
    # The modulo operator (%) ensures the index wraps around your list safely
    # e.g., 0%3=0, 1%3=1, 2%3=2, 3%3=0, 4%3=1...
    from_number = twilio_caller_ids[index % len(twilio_caller_ids)]
    
    try:
        print(f"[{index + 1}/{len(target_recipients)}] Dialing {target_number} from {from_number}...")
        
        call = client.calls.create(
            to=target_number,
            from_=from_number,
            url=twiml_url
        )
        
        print(f"    -> Call initiated successfully. SID: {call.sid}")
        
        # Pause briefly to respect Twilio's standard Calls Per Second (CPS) limits
        time.sleep(20)
        
    except TwilioRestException as e:
        print(f"    [!] Twilio Error calling {target_number}: {e.message}")
    except Exception as e:
        print(f"    [!] Unexpected Error: {e}")

print("\n--- Broadcast complete ---")
