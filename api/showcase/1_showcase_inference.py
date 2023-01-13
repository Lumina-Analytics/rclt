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
API_TOKEN = "PASTE TOKEN HERE"

# 2 SET TRAINING SESSION KEY HERE
SESSION_KEY = "000000001"

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
