from typing import Any
from pathlib import Path
import re
import os
import multiprocessing

# SCRIPT INSTRUCTIONS
# THIS SCRIPT WILL WORK FOR CCMATRIX AND TATOEBA DATASETS, INITIALLY THE SCRIPT IS CONFIGURED FOR TATOEBA SPANISH TO ENGLISH
# THE SCRIPT HAS BOTH GENERAL - LANGUAGE AGNOSTIC CLEANSING STEPS AS WELL AS LANGUAGE SPECIFIC CLEANSING STEPS
#   LANGUAGE AGNOSTIC CLEANSING ROUTINES:
#        cleanse_punctuation
#        cleanse_multistop
#        clean_general_characters
#   LANGUAGE SPECIFIC CLEANSING ROUTINES:
#        clean_input_to_language
#        clean_input_from_language
# FOLLOW THE INSTRUCTIONS BELOW TO CONFIGURE THE SCRIPT TO SUIT YOUR CASE

# 1 
# SET THE DELIMITER FOR THE FILE, EXAMPLES ARE TAB SEPERATED, DELIMITER INITIALLY SET TO <Tab>
# EXAMPLES USE TATOEBA and CCMATRIX, USE THE EXAMPLE INDEXES BELOW THAT BEST SUITS YOUR CASE, COMMENT THOSE THAT DO NOT

# 2 
# SET THE COLUMN INDEX FOR THE FROM LANGUAGE
# SET THE COLUMN INDEX FOR THE TO LANGUAGE

# 3 
# SET DATA_FOLDER SOURCE DATA (INPUT)
# SET OUTPUT_FOLDER CLEANSED DATA FOLDER (OUTPUT)

# 4
# COMMENT OUT THE LANGUAGE SPECIFIC VARIABLES YOU WILL NOT NEED AND UNCOMMENT THE LANGUAGE YOU INTEND TO TRAIN
# VALID_FROM_CHARS desc:  if the sentence doesn't match, the sentence is dropped from the training set, assumed to be "invalid language data".
# VALID_FROM_START_CHARS desc:  if the sentence doesn't start with a character from this set, the sentence is dropped from the training set, assumed to be "invalid language data".

# 5
# COMMENT OUT THE LANGUAGE SPECIFIC VARIABLES YOU WILL NOT NEED AND UNCOMMENT THE LANGUAGE YOU INTEND TO TRAIN
# VALID_TO_CHARS desc: similar to VALID_FROM_CHARS, rules applied to TRANSLATION_TO_LANGUAGE
# VALID_TO_START_CHARS desc: similar to VALID_FROM_START_CHARS, rules applied to TRANSLATION_TO_LANGUAGE

# SCRIPT SETUP
# 1
DELIMITER = "\t"

# 2
# FOR TATOEBA
FROM_LANGUAGE_INDEX = 1
TO_LANGUAGE_INDEX = 3

# FOR CC-MATRIX
# FROM_LANGUAGE_INDEX = 1
# TO_LANGUAGE_INDEX = 2

# 3
# DANISH
DATA_FOLDER = "example_data/tatoeba/danish/split" # SOURCE DATA (INPUT)
OUTPUT_FOLDER = "example_data/tatoeba/danish/cleansed" # CLEANSED DATA FOLDER (OUTPUT)
LOG_OUTPUT_FILE = Path("example_data/tatoeba/danish/log/log.txt") # LOGS REASONS DROP REASONS FOR TRAINING DATA

# SPANISH
# DATA_FOLDER = "example_data/tatoeba/spanish/split" # SOURCE DATA (INPUT)
# OUTPUT_FOLDER = "example_data/tatoeba/spanish/cleansed" # CLEANSED DATA FOLDER (OUTPUT)
# LOG_OUTPUT_FILE = Path("example_data/tatoeba/spanish/log/log.txt") # LOGS REASONS DROP REASONS FOR TRAINING DATA

# 4
# FROM LANGUAGE
# DANISH
VALID_FROM_CHARS_PATTERN = re.compile(r'(?:^[a-zA-Z0-9.,;0\/!?ÆØÅæøå\-\' ]*$)', re.RegexFlag.S) # non matching pattern
VALID_FROM_START_CHARS_PATTERN = re.compile(r'(^[a-zA-Z0-9ÆØÅæøå])') # matching pattern

# SPANISH
# VALID_FROM_CHARS_PATTERN = re.compile(r'(?:^[a-zA-Z0-9.,;0\/!?ÁÉÍÓÚÜÑáéíóúüñ¿¡\-\' ]*$)', re.RegexFlag.S) # non matching pattern, if any character hits, the sentence is invalid
# VALID_FROM_START_CHARS_PATTERN = re.compile(r'(^[a-zA-Z0-9!?ÁÉÍÓÚÜÑáéíóúüñ¿¡])') # if the sentence does not begin with one of these characters, the sentence is invalid and dropped from training

# 5 
# TO LANGUAGE
# ENGLISH
VALID_TO_CHARS_PATTERN = re.compile(r'(?:^[a-zA-Z0-9.,;0\/!?\-\' ]*$)', re.RegexFlag.S) # non matching pattern
VALID_TO_START_CHARS_PATTERN = re.compile(r'(^[a-zA-Z0-9])') # matching pattern
INVALID_TO_PUNCTUATION_PATTERN = re.compile(r'(^[ ][;,?!.])')

def LogLine(input:str):
    with open(file=LOG_OUTPUT_FILE, mode="a", encoding="utf-8") as f:
        f.write(input)

def cleanse_punctuation(input:str):
    # routine deduplicates ending punctuation such as ...
    # routine also removes punctuation in the form of punct1punct2 e.g. ;!
    # it is an imperfect routine that is handling unique but seldomly found occurrences in bitext dataset(s)
    repeating_punctuation = re.search(r"(\.|\?|\!)\1+", input) #handles repeating punctuation
    erroneous_punctuation = re.search(r"(\.\;\.\.\.\?\.\!|\;\.\;\;\;\?\;\!|\!\.\!\;\!\?\!\!|\?\.\?\;\?\?\?\!)", input) #handles grouped punctuation e.g. .; or ;? etc.
    invalid_punctuation = INVALID_TO_PUNCTUATION_PATTERN.search(input) #handles punctuation with a preceding space, in this case we simply drop the line from the training set
    punct = {".", "?", "!"}

    if repeating_punctuation:
        repeat_char = repeating_punctuation.group(0)[0]
        cleansed = input.replace(repeating_punctuation.group(0), repeat_char)
        input = cleansed

    if erroneous_punctuation:
        repeat_char = erroneous_punctuation.group(0)[0]
        cleansed = input.replace(erroneous_punctuation.group(0), repeat_char)
        input = cleansed
    
    if invalid_punctuation:
        LogLine(f"invalid_punctuation\t{input}\n")
        input = ""        

    if len(input) > 0 and input[-1] not in punct:
        LogLine(f"no_punctuation\t{input}\n")
        input = ""        

    return input

def clean_general_characters(input):
    # this routine cleans general characters that may reduce comprehension in translation.

    rem = re.compile(r'['
        u"\U0000200E" # L2R
        u"\U00000000" # null
        u"\U0000201C" # “
        u"\U0000201D" # ”
        u"\U0000003A" # :
        u"\U00000022" # "
        u"\U000000AB" # «
        u"\U000000BB" # »
        u"\U00002018" # left ‘
        u"\U00002019" # right ‘
        u"\U00002026" # horizontal ellipsis
        u"\U00002190-\U000021FF"  # arrows
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    + ']', re.UNICODE)
    input = re.sub(rem, '', input)
    return input
    
def clean_input_to_language(input):
    '''applies specific rules to the translate to language'''
    input = clean_general_characters(input)

    input = cleanse_punctuation(input)
    
    # if the sentence does not start with valid chars, eject it from training set
    if not re.match(VALID_TO_START_CHARS_PATTERN, input):
        LogLine(f"invalid_to_start_chars_pattern\t{input}\n")
        return ""
    
    # using non capturing group ?:
    # if we do not match, then drop the sentence
    if not re.match(VALID_TO_CHARS_PATTERN, input):
        LogLine(f"invalid_to_chars_pattern\t{input}\n")
        return ""
    
    return input

def clean_input_from_language(input):
    '''applies specific rules to the translate from language'''
    input = clean_general_characters(input)

    input = cleanse_punctuation(input)
    
    # if the sentence does not start with valid chars, eject it from training set  
    if not re.match(VALID_FROM_START_CHARS_PATTERN, input):
        LogLine(f"invalid from lang characters\t{input}\n")
        return ""

    # using non capturing group ?:
    # if we do not match, then drop the sentence
    if not re.match(VALID_FROM_CHARS_PATTERN, input):
        LogLine(f"invalid from lang characters\t{input}\n")
        return ""
    
    return input

def cleanse_align_ends(from_lang: str, to_lang:str):
    '''aligns the to_language end char to the from_language end char'''
    
    if len(from_lang) == 0 or len(to_lang) == 0:
        return "", ""

    from_lang_end = from_lang[-1]
    
    to_lang = to_lang[0: len(to_lang) - 1: 1] + from_lang_end

    return from_lang, to_lang

def cleanse_align_starts(from_lang: str, to_lang:str):
    '''aligns the to_language and from_language start chars.  Both from_lang and to_lang must both start with alpha or both start with numeric and be of the same case sensitivity to be accepted for training'''   
    if len(from_lang) == 0 or len(to_lang) == 0:        
        return "", ""

    from_lang_start = from_lang[0]
    to_lang_start = to_lang[0]

    if from_lang_start.isnumeric() and to_lang_start.isnumeric():
        return from_lang, to_lang

    if from_lang_start.isnumeric() and not to_lang_start.isnumeric():
        LogLine(f"mismatched start characters failed numeric check\t FROM:{from_lang} - TO:{to_lang}\n")
        return "", ""

    if not from_lang_start.isnumeric() and to_lang_start.isnumeric():
        LogLine(f"mismatched start characters failed numeric check\t FROM:{from_lang} - TO:{to_lang}\n")
        return "", ""

    # both sentences have matching lower case start
    if from_lang_start.islower() and to_lang_start.islower():
        return from_lang, to_lang

    # both sentences have matching upper case start
    if from_lang_start.islower() == False and to_lang_start.islower() == False:
        return from_lang, to_lang
        
    LogLine(f"mismatched start characters\t FROM:{from_lang} - TO:{to_lang}\n")
    return "", ""
    

def clean_line(line: str) -> str:
    '''cleans the sentence pair'''
    parts = line.split(DELIMITER)
    
    if len(parts) > 1:
        from_lang = parts[FROM_LANGUAGE_INDEX]
        to_lang = parts[TO_LANGUAGE_INDEX]

        # encode as utf-8    
        from_lang_bytes = from_lang.encode('utf-8')
        to_lang_bytes = to_lang.encode('utf-8')      

        from_lang = clean_input_from_language(from_lang_bytes.decode('utf-8')).strip()
        to_lang = clean_input_to_language(to_lang_bytes.decode('utf-8')).strip()

        lang_parts = cleanse_align_ends(from_lang, to_lang)
        from_lang = lang_parts[0]
        to_lang = lang_parts[1]

        lang_parts = cleanse_align_starts(from_lang, to_lang)
        from_lang = lang_parts[0]
        to_lang = lang_parts[1]
        
        if from_lang == "" or to_lang == "":
            text = ""
        else:
            text = f"{from_lang}\t{to_lang}"
            
            # OPTIONAL LOWER CASE THE LINE
            # text = text.lower()

        return text
    LogLine(f"unable to split by delimiter\t\n")
    return "" # drop rule hit invalid delimiter split

def unique_lines(lines: list[str]):
    new_lines = []
    new_lower_compressed_lines = []
    for line in lines:
        new_line = clean_line(line)
        if new_line.strip() != "":
            lower = new_line.lower().replace(" ", "") # let's deduplicate by lowered, but keep case
            if lower not in new_lower_compressed_lines:
                new_lower_compressed_lines.append(lower)
                new_lines.append(new_line)
            else:
                LogLine(f"dropped duplicate\t{new_line}\n")

    return new_lines

def clean_dataset(file: str) -> str:
    
    print(f'Working on file {file}')

    """Cleans a Tab seperated dataset for training purposes"""
    file_path = Path(f"{DATA_FOLDER}/").resolve().joinpath(file)

    file = Path(file_path)

    output_dir = Path(f"{OUTPUT_FOLDER}/").resolve()
    
    new_file = output_dir / f"{file.stem}_Cleansed.txt"
    
    lines = file.read_text(encoding="utf-8").strip().split("\n")

    text = "\n".join(unique_lines(lines))

    new_file.write_text(text, encoding="utf-8")
    
    print(f'Completed File {file}')

    return new_file

def file_read_Task(file:str):
    clean_dataset(file)

def clean_example_parallel():
    LogLine(f"Main\tProcess Starting\tfile cleanse\t{DATA_FOLDER}\n")
    
    #parallel process files in batches of 20
    training_files = os.listdir(DATA_FOLDER)
    
    with multiprocessing.Pool(30) as pool:
        pool.map(clean_dataset, training_files)

if __name__ == "__main__":
    # required for parallel processing
    clean_example_parallel()