from typing import Any
import requests
import json
import time

# This example script demonstrates how to reboot an inference host
# SET THE FOLLOWING VARIABLES
# 1. API_TOKEN (retrieve from the support portal @ https://support.lumina247.com)
# 2. SET SESSION_KEY this is the session_key for your trained model

API_URL = "https://testrclapi.lumina247.io"

API_TOKEN = "PASTE TOKEN HERE"

SESSION_KEY = "PASTE SESSION KEY HERE"

HEADERS = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Authorization": API_TOKEN,
}

def status_host():
    endpoint = (
        f"{API_URL}"
        f"/inferencehost/{SESSION_KEY}"
        f"/status"
    )

    try:
        response = requests.get(endpoint, data=json.dumps(SESSION_KEY), headers=HEADERS)
        
        if response.status_code != 200:
            raise Exception(f"Error calling inference: {response.json()}")
        else:
            status_dict = response.json()
            status = status_dict['actionState']
            print(f"Inference host status: {status}")
            return status
    except:
        raise Exception(f"A network error has occurred, unable to communicate with the api, check network connection and try again.")


def reboot_host():
    endpoint = (
        f"{API_URL}"
        f"/inferencehost/{SESSION_KEY}"
        f"/reboot"
    )

    try:
        response = requests.post(endpoint, data=json.dumps(SESSION_KEY), headers=HEADERS)
        
        if response.status_code != 200:
            raise Exception(f"Error calling inference: {response.json()}")
        else:
            status_dict = response.json()
            status = status_dict['actionState']
            print(f"Inference host status: {status}")
            return status
    except:
        raise Exception(f"A network error has occurred, unable to communicate with the api, check network connection and try again.")


if __name__ == "__main__":
    status = reboot_host()
    while status != 'running':
        status = status_host()
        time.sleep(2)