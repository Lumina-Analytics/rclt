from typing import Any
import requests
from pathlib import Path
import os
import time

# THIS SCRIPT TRAINS A NEW MODEL FOR TRANSLATION
# PLEASE SET THE FOLLOWING VARIABLES
# 1. API_TOKEN (retrieve from the support portal @ https://support.lumina247.com)
# 2. SET VECTOR_SIZE this is the vector size you used for training
# 3. SET THE FILE_UPLOAD_CHUNK_SIZE TO THE TOTAL BYTE SIZE CHUNK FOR UPLOAD, DEFAULT SHOULD BE SUFFICIENT HERE
# 4. NAME YOUR TRAINING SESSION
# 5. CHOOSE A LANGUAGE FROM THE OPTIONS BELOW COMMENT OUT THE VARIABLES FOR THE LANGUAGES YOU WILL NOT NEED AND UNCOMMENT THE VARIABLES FOR LANGUAGE YOU INTEND TO TRAIN

API_URL = "https://testrclapi.lumina247.io"

# 1 example: bearer <token>
API_TOKEN = "PASTE TOKEN HERE"

# 2
VECTOR_SIZE = 5

# 3
FILE_UPLOAD_CHUNK_SIZE = 50000000

# 4
# DANISH
TRAINING_SESSION_NAME = "DANISH_TATOEBA_EXAMPLE"

# SPANISH
# TRAINING_SESSION_NAME = "SPANISH_TATOEBA_EXAMPLE"

# 5
# LANGUAGE VARIABLES
# DANISH
DATA_FOLDER = "example_data/tatoeba/danish/reversed"

# SPANISH
# DATA_FOLDER = "example_data/tatoeba/spanish/reversed"

HEADERS = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Authorization": API_TOKEN,
}

def parse_api_response(response: requests.Response) -> dict[str, Any]:
    """extracts json from response and raises errors when needed"""
    if response.status_code > 200:
        raise Exception("Error calling api")
    return {k.lower(): v for k, v in response.json().items()}

def create_session(description: str) -> int:
    """Creates an RCL session and returns the id"""
    endpoint = f"{API_URL}/trainingsession"
    try:
        response = requests.post(
            endpoint, json={"description": str(description)}, headers=HEADERS)
        return parse_api_response(response).get("trainingsessionkey", -1)
    except:
        raise Exception(f"Api Communication failure, unable to create session, check network connection and try again.")
    

def get_session_info(session_key: int) -> dict[str, Any]:
    """Gets info about an rcl session"""
    response = requests.get(
        f"{API_URL}/trainingsession/{session_key}", headers=HEADERS)
    result = parse_api_response(response)
    try:
        return result
    except:
        raise Exception(f"Session {session_key} does not exist!")

def _multipart_upload_start(session_key: int, file_name: str) -> str:
    """Gets an id for a future file upload"""
    endpoint = f"{API_URL}/trainingsession/{session_key}/document/upload/multipart/{file_name}"
    
    print(f"Initializing Multipart upload")

    try:
        response = requests.post(endpoint, headers=HEADERS)
        result = parse_api_response(response)
        return result["documentid"]
    except:
        raise Exception(f"Api Communication failure, unable to start multipart upload, check network connection and try again.")
    

def _multipart_upload_chunk(
    session_key: int,
    document_id: str,
    content: bytes,
    part_number: int = 1,
    last_part: bool = True,
) -> bool:
    """Uploads a part of a multipart file"""
    endpoint = (
        f"{API_URL}"
        f"/trainingsession/{session_key}"
        f"/document/{document_id}"
        f"/upload/multipart/{part_number}/{last_part}"
    )        

    try:
        response = requests.put(
            endpoint,
            data=content,
            headers={
                "Content-Type": "application/octet-stream",
                "Authorization": API_TOKEN,
            },
        )
        return response.status_code == 200
    except:
        raise Exception(f"Api Communication failure, unable to upload chunk, check network connection and try again.")   

def _multipart_upload_complete(session_key: int, document_id: str) -> bool:
    """Marks a multipart upload as complete"""
    endpoint = (
        f"{API_URL}"
        f"/trainingsession/{session_key}"
        f"/document/{document_id}/upload/multipart/complete"
    )
    
    print(f"Finalizing Multipart upload")

    try:
        response = requests.post(
            endpoint,
            headers=HEADERS,
            json={},
        )
        return response.status_code == 200
    except:
        raise Exception(f"Api Communication failure, unable to complete multipart upload, check network connection and try again.")
    
def read_in_chunks(file_object, CHUNK_SIZE):
    
    print(f"Chunking upload, chunk_size: {CHUNK_SIZE}")

    while True:
        data = file_object.read(CHUNK_SIZE)
        if not data:
            break
        yield data
   
def upload_training_files(session_key: int, file: Path) -> bool:
    """Uploads a file by path"""    
    
    file_path = os.path.abspath(file)

    file_id = _multipart_upload_start(session_key, file.name)
   
    index = 0
    file_object = open(file_path, "rb")
    chunks = list(read_in_chunks(file_object, FILE_UPLOAD_CHUNK_SIZE))
    total_chunks = len(chunks)
    
    for chunk in chunks:
        try: 
            index = index + 1
            
            last_part = index == total_chunks
            
            print(f"Uploading chunk: {index} of {total_chunks}")
            
            ok = _multipart_upload_chunk(
                session_key,
                file_id,
                chunk,
                index,
                last_part
            )

            if not ok:
                return False

        except Exception as e:
            print(e)
            return False
    
    _multipart_upload_complete(
        session_key,
        file_id,
    )

    return True

def check_training_failed(session_key: int):
    '''checks if training has failed'''
    try:
        response = requests.get(f"{API_URL}/trainingsession/{session_key}",
        headers=HEADERS)
    
        stats = response.json()['trainingSession']['statuses']
    
        training_failed = False
    
        for stat in stats:
            if stat['statusType'] == "TrainingFailed":
                training_failed = True

        if(training_failed):
            print('Training did not succeed')

        return training_failed
    except:
        raise Exception(f"Api Communication failure, unable to check training failed status, check network connection and try again.")

def check_training_succeeded(session_key: int):
    '''checks if training has completed successfully'''
    try:
        response = requests.get(f"{API_URL}/trainingsession/{session_key}",
            headers=HEADERS)
        
        stats = response.json()['trainingSession']['statuses']
        
        training_succeeded = False
        
        for stat in stats:
            if stat['statusType'] == "TrainingCompleted":            
                training_succeeded = True

        if(training_succeeded):
            print('Training succeeded')

        return training_succeeded   
    except:
        raise Exception(f"Api Communication failure, unable to check training succeeded status, check network connection and try again.")

def check_training_status(session_key: int):
    '''checks all statuses for a training session and returns the latest status'''
    try:
        response = requests.get(f"{API_URL}/trainingsession/{session_key}",
            headers=HEADERS)
        
        stats = response.json()['trainingSession']['statuses']
        
        training_statuses = []
        
        for stat in stats:
            training_statuses.append(stat['statusType'])
        
        last_training_status = training_statuses[-1]
        
        return last_training_status  
    except:
        raise Exception(f"Api Communication failure, unable to check training status, check network connection and try again.")

def train_model(
    session_key: int,
    vector_size: int,
    translation_model: bool = True,
    sensor_model: bool = False,
    train_goal: float = 0.7
) -> bool:
    """Trains the RCL Model with the provided settings"""
    try:
        response = requests.post(
            f"{API_URL}/trainingsession/{session_key}/start",
            json={ 
                "vectorSize": vector_size,
                "trainTranslationServices": translation_model,
                "trainSensorServices": sensor_model,
                "trainGoal": train_goal,
            },
            headers=HEADERS,
        )

        if response.status_code != 200:
            raise Exception(f"Training error occurred, response code is {response.status_code}")
        
        training_succeeded = False
        training_failed = False

        while(training_failed == False and training_succeeded == False):
            training_failed = check_training_failed(session_key)
            training_succeeded = check_training_succeeded(session_key)
            training_status = check_training_status(session_key)
            print("Training Session Status:", training_status)
            time.sleep(60) 
    except:
        raise Exception(f"Api Communication failure, check network connection and try again.")


def translation_training_example():
    """End to end example for translation and gleu scoring"""

    session_key = create_session(TRAINING_SESSION_NAME)
    
    print(f"Created session: {session_key}")   

    training_files = os.listdir(DATA_FOLDER)

    for file in training_files:            
        print(f"Cleaning file {file} before upload.")

        dataset = Path(f"{DATA_FOLDER}/").resolve().joinpath(file)

        upload_training_files(session_key, dataset)

    print("Upload Completed, Beginning Training")

    training_successful = train_model(session_key, VECTOR_SIZE, translation_model=True)

    if training_successful == False:
        print("Training did not complete successfully")
        return
    
    if training_successful == True:
        print("Training completed successfully")
        return

    print("Training ended")

if __name__ == "__main__":
    translation_training_example()