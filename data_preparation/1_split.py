from typing import Any
from pathlib import Path
import math

# SCRIPT INSTRUCTIONS
# THIS OPTIONAL SCRIPT WILL ASSIST IN PROCESSING VERY LARGE DATAFILES
# 1 SET THE OUTPUT_FOLDER, THIS IS WHERE YOUR OUTPUT FILES WILL BE STORED
# 2 SET THE DATA_SET, THIS IS THE SOURCE FILE TO BE SPLIT
# 3 SET THE VARIABLE TOTAL_FILE_COUNT = THE NUMBER OF FILES YOU DESIRE TO SPLIT TO, THE LARGER THIS NUMBER THE SMALLER THE RESULTING FILES WILL BE, BUT ALSO THE MORE NUMEROUS THEY WILL BE

# SCRIPT SETUP
# 1
OUTPUT_FOLDER = "example_data/tatoeba/spanish/split"

# 2
# DANISH
# DATA_SET = "example_data/tatoeba/spanish/unmodified/Sentence pairs in Danish-English.tsv"

# SPANISH
DATA_SET = "example_data/tatoeba/spanish/unmodified/Sentence pairs in Spanish-English.tsv"

# 3
TOTAL_FILE_COUNT = 2

def write_file(lines: list[str], iteration: int, file: Path):
    '''Writes the lines out to a new file'''
    new_file = Path(f"{OUTPUT_FOLDER}/").resolve().joinpath(f"{file.stem}_{iteration}{file.suffix}")
    text = "\n".join(lines)
    new_file.write_text(text, encoding="utf-8")

def split_large_file():
    '''Split a large file into several smaller files for processing'''
    print("loading large file, please wait...")
    file = Path(DATA_SET)
    lines = file.read_text(encoding="utf-8").strip().split("\n")
    lines_per_file = math.ceil(len(lines) / TOTAL_FILE_COUNT)
    current_iteration = 1
    current_line_count = 0
    line_bucket = []
    lines_remaining = len(lines)

    for line in lines:        
        current_line_count = current_line_count + 1        
        lines_remaining = lines_remaining - 1
        
        print(f"lines remaining: {lines_remaining}")

        if(current_line_count < lines_per_file and lines_remaining != 0):
            line_bucket.append(line)
        else:
            write_file(line_bucket, current_iteration, file)
            current_line_count = 0
            current_iteration = current_iteration + 1
            line_bucket.clear()
            

if __name__ == "__main__":
    split_large_file()