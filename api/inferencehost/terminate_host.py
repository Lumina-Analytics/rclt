from typing import Any
import requests
import json
import time

# WARNING: TERMINATING YOUR INFERENCE HOST WILL STOP YOUR ABILITY TO INFER FROM YOUR MODEL PERMANENTLY, YOU WILL NOT BE ABLE TO UNDO THIS ACTION

# This example script demonstrates how to terminate an inference host
# SET THE FOLLOWING VARIABLES
# 1. API_TOKEN (retrieve from the support portal @ https://support.lumina247.com)
# 2. SET SESSION_KEY this is the session_key for your trained model

API_URL = "https://rclapi.lumina247.io"

API_TOKEN = "bearer eyJraWQiOiJpZzA2bDFkQjhlQkUxanAxN0tkYTMxUlVNVEM4QVpVdXVFVGd4aHQ1ZWQ0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4YWI3MzUxOC1mYjhhLTQ1YmUtYmEzNC0wMzYxYjdkYzNjMTYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9zYkNlc1k5eWMiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIzcDM2c2xsZTc1ZjYzcXJpMHRhczZldG9zNSIsIm9yaWdpbl9qdGkiOiI5OTYzYTBiZC01YjVlLTQ1YzEtOWNkZS1lYzc5OTcwMjk2YmUiLCJldmVudF9pZCI6IjA5Mjc5N2NhLTM1N2MtNGY1Ni05ZjE0LWNmMDFkYjBmNjFlMSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUiLCJhdXRoX3RpbWUiOjE2NzMyOTQwMjQsImV4cCI6MTY3MzM4MDQyOCwiaWF0IjoxNjczMjk0MDI5LCJqdGkiOiI5NWQ1MWYxNy1mZjM1LTQ5NDYtOGFhZS04NDE3NTkxNjZjYWEiLCJ1c2VybmFtZSI6IjhhYjczNTE4LWZiOGEtNDViZS1iYTM0LTAzNjFiN2RjM2MxNiJ9.XeKfxrHb_6lorPF4vdpXVe4lOrqbNrlfikf16ubUxdrpD35HWu-6Ay_HT01aFT0kbvppW9WTD-bxDReU7IGBFL1KJD7nqx2SmrBYGCIiPDYw2ns_9KooMHDm1qKGVbcR2vm4lK1AxB81oFiSkAHYQ7q1aNlYgW2cNK8R-OzCxxaxVREzh0gVCIVjehm4lzNslk2MgK36byqK9Fh-r9V0HXX8vQ4FtN_un9qWgZj2EFh5ViXhAzUZz2nNHDCf8KHqj4Hb2ee1kFxk4-qvhhq2F5AS9OMd1nEkdc96f0V7ugfVCkeP4HJnN7eZgB8-0mHSRL2ebrQhNJbHSQjTerxYkw"

SESSION_KEY = "121669978"

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


def terminate_host():
    endpoint = (
        f"{API_URL}"
        f"/inferencehost/{SESSION_KEY}"
        f"/terminate"
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
    status = terminate_host()
    while status != 'terminated':
        status = status_host()
        time.sleep(2)