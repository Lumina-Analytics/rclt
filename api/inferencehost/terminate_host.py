from typing import Any
import requests
import json


# WARNING: TERMINATING YOUR INFERENCE HOST WILL STOP YOUR ABILITY TO INFER FROM YOUR MODEL PERMANENTLY, YOU WILL NOT BE ABLE TO UNDO THIS ACTION

# This example script demonstrates how to terminate an inference host
# SET THE FOLLOWING VARIABLES
# 1. API_TOKEN (retrieve from the support portal @ https://support.lumina247.com)
# 2. SET SESSION_KEY this is the session_key for your trained model

API_URL = "https://rclapi.lumina247.io"
API_TOKEN = "bearer"
SESSION_KEY = ""

HEADERS = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Authorization": API_TOKEN,
}

def terminate_host():
    endpoint = (
        f"{API_URL}"
        f"/inferencehost/{SESSION_KEY}"
        f"/terminate"        
    )

    r = requests.post(endpoint, data=json.dumps(SESSION_KEY), headers=HEADERS)
    
    if r.status_code != 200:
        raise Exception(f"Error calling inference: {r.json()}")
    else:
        print('INFERENCE HOST TERMINATED')

if __name__ == "__main__":
    terminate_host()