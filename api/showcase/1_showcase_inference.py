from typing import Any
import requests
import json
from enum import Enum
from requests import Response
import time
from pathlib import Path

# This example script demonstrates how to infer from a trained model published to the rcl showcase.
# The service will automatically start a new host for inference, wait for the host to be ready and then execute an example inference request.
# You will want to extend this example for multiple inference or to programatically include in your own applications
# PLEASE SET THE FOLLOWING VARIABLES
# 1. API_TOKEN (retrieve from the support portal @ https://support.lumina247.com)
# 2. SET SESSION_KEY this is the session_key for your trained model
# 3. SET The Showcase Revision Number
# 4. SET TEST_DATA_SOURCE this is the path to your test data for inference

API_URL = "https://rclapi.lumina247.io"

# 1 example: bearer <token>
API_TOKEN = "bearer eyJraWQiOiJpZzA2bDFkQjhlQkUxanAxN0tkYTMxUlVNVEM4QVpVdXVFVGd4aHQ1ZWQ0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4YWI3MzUxOC1mYjhhLTQ1YmUtYmEzNC0wMzYxYjdkYzNjMTYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9zYkNlc1k5eWMiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIzcDM2c2xsZTc1ZjYzcXJpMHRhczZldG9zNSIsIm9yaWdpbl9qdGkiOiIwMmI5YjRlNS1lNzFlLTQyNTctOWZmYS1kNDFiMDhmMzU1M2EiLCJldmVudF9pZCI6IjMwNmZmNmYzLWIxYWYtNDc5ZS1hMDQ1LWQzOWY2MmFmZjA1ZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUiLCJhdXRoX3RpbWUiOjE2NzM2Mjg1OTcsImV4cCI6MTY3MzcxNTAwMCwiaWF0IjoxNjczNjI4NjAwLCJqdGkiOiI0ODYyNDU5MS01N2Y2LTQ0MzEtYjkxZC01OThkODRlODllNmIiLCJ1c2VybmFtZSI6IjhhYjczNTE4LWZiOGEtNDViZS1iYTM0LTAzNjFiN2RjM2MxNiJ9.Zd3Htc6XdyM9UFQ2YcrKbdYHaXPwkNObHWbTnT371AzE_ZUfFd_5GOur26SpP1aFK_77bKY1B1uHuT9GVnYDFHShu7lY4KJ-0mMWD9Jekorq2477W3HiaxAdeRS0NIETIcda9PFAhJca7-VcjxDFw0dHuaz8gUtr7sGF-7-8SNTZzJ5TdeZMq4MdogV_akOxoJuvmp2xabCFmxxcbBwdZBkWeiNaRAb_Kwrkovo04O92FmTPnizhTMtsmhYov5aTK98wZ6VJg_EWc4WboWBbwW24LVf_RgGvw13Lekfe-bw8asFZSTPIGtdROyqA9agi_erlvzIwiY_iV1DFx9uegw"

# 2 SET TRAINING SESSION KEY HERE
SESSION_KEY = "127758762"

REVISION_NUMBER = "1"

# 3 SET TEST DATA
# Danish
TEST_DATA_SOURCE = "example_data/tatoeba/danish/test_data/test_data_Cleansed_r.txt"

HEADERS = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Authorization": API_TOKEN,
}

class InferenceDetailType(Enum):
    """Enums containing the id's for inference types"""
    search = "Search"
    predict_line = "PredictLine"
    predict_next = "PredictNext"
    translate_line = "TranslateLine"
    hot_word = "HotWord"

class InferencePriorityType(Enum):
    """Enums containing the id's for training optimizers"""
    index = "Index"
    accuracy = "Accuracy"
    specific = "Specific"

def parse_api_response(response: requests.Response) -> dict[str, Any]:
    """extracts json from response and raises errors when needed"""
    if response.status_code > 200:
        raise Exception("Error calling api")
    return {k.lower(): v for k, v in response.json().items()}
 
def translate_inference_example(
    input_text: str,
    priority: InferencePriorityType = InferencePriorityType.index,
    detail: InferenceDetailType = InferenceDetailType.translate_line,
) -> str:
    """Makes an inference with the model"""
    endpoint = (
        f"{API_URL}"
        f"/showcase/{SESSION_KEY}"
        f"/inference/{priority.value}"
        f"/{REVISION_NUMBER}"
        f"/{detail.value}"
    )

    try:
        response = requests.post(endpoint, data=json.dumps(input_text), headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error calling inference: {response.json()}")
    except:
        raise Exception(f"Error calling inference server: {response.json()}, check network connection and try again")

def test_showcase_inference(): 
    test_file = Path(TEST_DATA_SOURCE)
    lines = test_file.read_text(encoding="utf8").strip().split("\n")

    for i in range(30):
        example_inference = lines[i].strip().split("\t")[0]

        print(example_inference)

        inference_result = translate_inference_example(example_inference)

        print(f"Inference Result: {inference_result['content']}")

if __name__ == "__main__":
    test_showcase_inference()
