from typing import Any
from pathlib import Path
import os

# SCRIPT INSTRUCTIONS
# THIS SCRIPT SIMPLY REVERSES A DATASET FOR BIDIRECTIONAL TRAINING, FOR INSTANCE YOUR SOURCE FILE IS CURRENTLY DANISH:ENGLISH, THIS SCRIPT WILL REVERSE THE ORDER TO ENGLISH:DANISH AND STORE IN THE CHOSEN DIRECTORY AS NEW FILES
# 1 CHOOSE A LANGUAGE FROM THE OPTIONS BELOW COMMENT OUT THE VARIABLES FOR THE LANGUAGES YOU WILL NOT NEED AND UNCOMMENT THE VARIABLES FOR LANGUAGE YOU INTEND TO TRAIN
# 2 SET THE DELIMITER FOR THE FILE TO BE PROCESSED 

# 1 LANGUAGE VARIABLES
# DANISH
DATA_FOLDER = "example_data/tatoeba/danish/deduplicated"
OUTPUT_FOLDER = "example_data/tatoeba/danish/reversed"

# SPANISH
# DATA_FOLDER = "example_data/tatoeba/spanish/deduplicated"
# OUTPUT_FOLDER = "example_data/tatoeba/spanish/reversed"

# 2 DELMITER
DELIMITER = "\t"

def cleanse_multistop(input:str):
    stop_char = input[-1]
    input_clear = input[0: len(input) - 1: 1]
    input = input_clear.replace(".", "")
    input = input.replace("?", "")
    input = input.replace('!', ' ')
    input = input + stop_char        
    return input

def reverse_dataset(path: str) -> str:
    """Cleans a Tab seperated dataset for training purposes"""
    def reverse_line(line: str) -> str:
        parts = line.split(DELIMITER)
        if len(parts) > 1:
            p1 = parts[0].strip()
            p2 = parts[1].strip()
        
            part1bytes = p1.encode('utf-8')
            part2bytes = p2.encode('utf-8')

            part1 = part1bytes.decode('utf-8').strip()
            part2 = part2bytes.decode('utf-8').strip()

            text = f"{part2}\t{part1}"

            return text
        return ""
    
    output_dir = Path(f"{OUTPUT_FOLDER}/").resolve()
    
    file = Path(path)
        
    new_file = output_dir / f"{file.stem}_r.txt"
    
    lines = file.read_text(encoding="utf-8").strip().split("\n")
    
    text = "\n".join([reverse_line(l) for l in lines])
    
    new_file.write_text(text, encoding="utf-8")        

def reverse_example_serial():
    training_files = os.listdir(DATA_FOLDER)

    for file in training_files:
        print(f"Reversing {file}")

        dataset = Path(f"{DATA_FOLDER}/").resolve().joinpath(file)

        clean_file = reverse_dataset(dataset)

if __name__ == "__main__":    
    reverse_example_serial()