import os
import time
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# 1. Initialize the Twilio Client with your single Account SID and Auth Token
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'AC2cb3d566b801721a41c7599f682a67d4')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '4512297ef74dc62507bd01b31b0b52d0')
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# 2. Define your pool of Twilio outbound numbers
twilio_caller_ids = [
    '+17179054291', 
    '+17178925593', 
    '+17178077317'
]

# 3. Define the list of recipients you want to call
target_recipients = [
    '+17178761447',
    '+17178761457',
    '+17178761503',
    '+17178761476',
    '+17178761424',
    '+17178761462',
    '+17178761486',
    '+17178761501',
    '+17178761495',
    '+17178761451',
    '+17178761481',
    '+17178761438',
    '+17178761415',
    '+17178761450',
    '+17178761420',
    '+17178761411',
    '+17178761446',
    '+17178761401',
    '+17178761499'	
]

# 4. Your audio instructions
audio_url = 'https://burp.digitaloffensive.com/pedo.mp3'
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
