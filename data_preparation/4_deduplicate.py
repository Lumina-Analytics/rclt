from typing import Any
from pathlib import Path

# SCRIPT INSTRUCTIONS
# THIS SCRIPT WILL DEDUPLICATE TRAINING DATA USING THE FOLLOWING RULES:
#   RULE 1: EXACT SENTENCE PAIR DUPLICATES, IF THE EXACT TO:FROM SENTENCE EXISTS
#   RULE 2: SENTENCE PAIR EXISTS WITH MORE THAN 1 TO LANGUAGE TRANSLATION, THE RESULT WITH THE "SHORTEST" TRANSLATION WILL BE CHOSEN, ALL OTHERS WILL BE IGNORED
#   RULE 2: SENTENCE PAIR EXISTS WITH MORE THAN 1 FROM LANGUAGE TRANSLATION, THE RESULT WITH THE "SHORTEST" TRANSLATION WILL BE CHOSEN, ALL OTHERS WILL BE IGNORED
# 1 CHOOSE A LANGUAGE FROM THE OPTIONS BELOW COMMENT OUT THE VARIABLES FOR THE LANGUAGES YOU WILL NOT NEED AND UNCOMMENT THE VARIABLES FOR THE LANGUAGE YOU INTEND TO TRAIN
#   INPUT_FILE: PATH TO FILE TO BE DEDUPLICATED
#   OUTPUT_FILE: FILE LOCATION TO STORE DEDUPLICATED RESULTS

# 1 LANGUAGE VARIABLES
# DANISH
# INPUT_FILE = "example_data/tatoeba/danish/combined/DA_EN.txt"
# OUTPUT_FILE = "example_data/tatoeba/danish/deduplicated/DA_EN.txt"

# SPANISH
INPUT_FILE = "example_data/tatoeba/spanish/combined/ES_EN.txt"
OUTPUT_FILE = "example_data/tatoeba/spanish/deduplicated/ES_EN.txt"

def deduplicate_lines_reverse(lines: dict):
    '''DEDUPLICATES FILE BASED ON TO LANGUAGE AND SHORTEST LENGTH FROM LANGUAGE'''
    lines_dict = {}    

    for key,value in lines.items():        
        from_lang = key
        to_lang = value
        from_lang_len = len(from_lang)

        if to_lang not in lines_dict.keys():
            lines_dict[to_lang] = from_lang
        else:
            current_translation_length = len(lines_dict[to_lang])
            if(current_translation_length >= from_lang_len):
                lines_dict[to_lang] = from_lang
    
    return lines_dict

def deduplicate_lines(lines: list[str]):
    '''DEDUPLICATES FILE BASED ON FROM LANGUAGE AND SHORTEST LENGTH TO LANGUAGE'''
    lines_dict = {}
    
    for line in lines:
        langs = line.split("\t")
        from_lang = langs[0]
        to_lang = langs[1]        
        to_lang_len = len(to_lang)

        if from_lang not in lines_dict.keys():
            lines_dict[from_lang] = to_lang
        else:
            current_translation_length = len(lines_dict[from_lang])
            if(current_translation_length >= to_lang_len):
                lines_dict[from_lang] = to_lang
    
    return lines_dict

def deduplicate_example() -> str:
    print(f'Working on file')
        
    file = Path(INPUT_FILE)    
    
    new_file = Path(OUTPUT_FILE)
    
    lines = file.read_text(encoding="utf-8").strip().split("\n")    

    deduplicated_lines = deduplicate_lines(lines)

    deduplicated_lines_reversed = deduplicate_lines_reverse(deduplicated_lines)

    text = "\n".join([f"{value}\t{key}" for key,value in deduplicated_lines_reversed.items()])
    
    new_file.write_text(text, encoding="utf-8")
    
    print(f'Completed File {file}')

    return new_file

if __name__ == "__main__":
    deduplicate_example()