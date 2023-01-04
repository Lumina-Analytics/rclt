from typing import Any
from pathlib import Path
import os

# SCRIPT INSTRUCTIONS
# THIS SCRIPT WILL RECOMBINE SPLIT FILES AND IS GENERALLY USEFUL FOR DEDUPLICATION OF A DATASET
# SET DATA_FOLDER = THE LOCATION OF THE FILES TO BE COMBINED
# SET OUTPUT_FILE_NAME = THE FILE LOCATION TO STORE THE COMBINED RESULTS

# DANISH
DATA_FOLDER = "example_data/tatoeba/danish/cleansed"
OUTPUT_FILE_NAME = "example_data/tatoeba/danish/combined/DA_EN.txt"

# SPANISH
# DATA_FOLDER = "example_data/tatoeba/spanish/cleansed"
# OUTPUT_FILE_NAME = "example_data/tatoeba/spanish/combined/ES_EN.txt"

def combine_files():
    training_files = os.listdir(DATA_FOLDER)
    
    new_file = Path(OUTPUT_FILE_NAME)

    for file in training_files:
        print(f"Combining {file}")               

        dataset = Path(f"{DATA_FOLDER}/").resolve().joinpath(file)

        lines = dataset.read_text(encoding="utf-8")
        
        text = "\n".join([lines]).encode("utf-8").decode("utf-8")
        
        with open(file=new_file, mode="a", encoding="utf-8") as nf:
            nf.write(text)

if __name__ == "__main__":
    combine_files()