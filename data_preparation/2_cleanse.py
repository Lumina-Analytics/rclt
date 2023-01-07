from typing import Any
from pathlib import Path
import re
from re import Pattern
import os
import multiprocessing

# CLEANSING SCRIPT INSTRUCTIONS
# FOLLOW THE INSTRUCTIONS BELOW TO CONFIGURE THE SCRIPT TO SUIT YOUR NEEDS

# 1 FILE_DELIMITER
# SET THE DELIMITER FOR THE FILE, EXAMPLES ARE TAB SEPERATED, DELIMITER INITIALLY SET TO <Tab>
# EXAMPLES USE TATOEBA and CCMATRIX, USE THE EXAMPLE INDEXES BELOW THAT BEST SUITS YOUR CASE, COMMENT THOSE THAT DO NOT

# 2 FILE_COLUMN INDEXES FOR SENTENCE PAIRS
# SET THE COLUMN INDEX FOR THE FROM LANGUAGE
# SET THE COLUMN INDEX FOR THE TO LANGUAGE

# 3 SET FOLDER LOCATIONS
# SET DATA_FOLDER SOURCE DATA (INPUT)
# SET OUTPUT_FOLDER CLEANSED DATA FOLDER (OUTPUT)

# 4 CONFIGURE FROM LANGUAGE SPECIFIC PATTERN VARIABLES
# COMMENT OUT THE LANGUAGE SPECIFIC VARIABLES YOU WILL NOT NEED AND UNCOMMENT THE LANGUAGE YOU INTEND TO TRAIN
# VALID_FROM_CHARS desc:  if the sentence doesn't match, the sentence is dropped from the training set, assumed to be "invalid language data".
# VALID_FROM_START_CHARS desc:  if the sentence doesn't start with a character from this set, the sentence is dropped from the training set, assumed to be "invalid language data".

# 5 CONFIGURE TO LANGUAGE SPECIFIC PATTERN VARIABLES
# COMMENT OUT THE LANGUAGE SPECIFIC VARIABLES YOU WILL NOT NEED AND UNCOMMENT THE LANGUAGE YOU INTEND TO TRAIN
# VALID_TO_CHARS desc: similar to VALID_FROM_CHARS, rules applied to TRANSLATION_TO_LANGUAGE
# VALID_TO_START_CHARS desc: similar to VALID_FROM_START_CHARS, rules applied to TRANSLATION_TO_LANGUAGE

# 6 PUNCTUATION PATTERNS
# INVALID_PUNCTUATION_PATTERN - This pattern is used to find punctuation we have found to effect translation quality in some datasets
# REPEATING_PUNCTUATION_PATTERN - This pattern is used to find repeating punctuation e.g. ... or ??
# GROUPED_PUNCTUATION_PATTERN - This pattern is used to find groups of punctuation we have found to effect translation quality in some datasets, e.g. ?! or !?
 
# 7 MAX PARALLEL PROCESSES - The maximum files to process in parallel, size according to your computers abilities to process in parallel, a larger number allows for faster processing.
# 8 CLEANSING RULES - Evaluate the rules in this section.  Depending on the languages to be translated, you may need to enable or disable these rules to suit your specific use case needs.

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

# 5 TO LANGUAGE SPECIFIC PATTERN VARIABLES
# TO LANGUAGE
# ENGLISH
VALID_TO_CHARS_PATTERN = re.compile(r'(?:^[a-zA-Z0-9.,;0\/!?\-\' ]*$)', re.RegexFlag.S) # non matching pattern
VALID_TO_START_CHARS_PATTERN = re.compile(r'(^[a-zA-Z0-9])') # matching pattern

# 6 PUNCTUATION PATTERNS
MALFORMED_PUNCTUATION_PATTERN = re.compile(r'(^[ ][;,?!.])')
REPEATING_PUNCTUATION_PATTERN = re.compile(r"(\.|\?|\!)\1+")
GROUPED_PUNCTUATION_PATTERN = re.compile(r"(\.\;\.\.\.\?\.\!|\;\.\;\;\;\?\;\!|\!\.\!\;\!\?\!\!|\?\.\?\;\?\?\?\!)")

# 7 MAX PARALLEL PROCESSES
MAX_PARALLELISM = 30

# 8 CLEANSING RULES
# RULE
# NOTE: DEDUPLICATION: This rule seeks to remove exact sentence pair duplicates from the training set.
ENABLE_RULE_DEDUPLICATION = True

# RULE: LOWERCASE
# NOTE: This rule will lowercase all data in the final output
ENABLE_RULE_LOWERCASE = True

# RULE(S): REMOVE_UNICODE: this routine cleans common unicode characters found in some of the example data, extend, reduce or disable this rule as needed.
# NOTE: This rule can be applied to one or both languages in a language pair
ENABLE_RULE_REMOVE_UNICODE_FROM_LANG = True
ENABLE_RULE_REMOVE_UNICODE_TO_LANG = True

# RULE(S): CLEANSE_REPEATING_PUNCTUATION
# NOTE: This rule will cleanse repeating punctuation e.g. ... will be mutated to .
ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_FROM_LANG = True
ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_TO_LANG = True

# RULE(S): CLEANSE_GROUPED_PUNCTUATION
# NOTE: This rule will cleanse grouped punctuation e.g. !? will be mutated to ?
ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_FROM_LANG = True
ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_TO_LANG = True

# RULE(S): CLEANSE_REPEATING_PUNCTUATION
# NOTE: This rule will cleanse malformed sentences, matches will be dropped from the training set.  e.g. Hi, good morning ! maybe dropped due to the space after morning
ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_FROM_LANG = True
ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_TO_LANG = True

# RULE: ALIGN PUNCTUATION
# NOTE: This rule will ensure that punctuation matches between the from lang and the to lang, for instance (hi, good morning!    Hola buenos días.) is mutated to (hi, good morning! Hola buenos días!)
ENABLE_RULE_ALIGN_PUNCTUATION = True

# RULE: ENSURE START ALIGNED
# NOTE: This rule will ensure that sentence pairs start with similar styles.
# NOTE: Ensures both sentences start with a numeric OR
# NOTE: Ensures both sentences start with a lower case alpha character
# NOTE: Ensures both sentences start with an upper case alpha character
# NOTE: This maybe an issue when converting from / to Spanish and you may consider disabling for this language set
ENABLE_RULE_ALIGN_START = True

# RULE: ENSURE FROM LANGUAGE START CHARACTER MATCH
# NOTE: This rule will ensure the from language starts with a valid character from that languages alphabet
ENABLE_RULE_FROM_LANGUAGE_START_VALIDATION = True

# RULE: ENSURE TO LANGUAGE START CHARACTER MATCH
# NOTE: This rule will ensure the to language starts with a valid character from that languages alphabet
ENABLE_RULE_TO_LANGUAGE_START_VALIDATION = True

# RULE: ENSURE FROM LANGUAGE CHARACTER MATCH
# NOTE: This rule will ensure the from language only contains characters defined in the VALID_FROM_CHARS_PATTERN
ENABLE_RULE_FROM_LANGUAGE_VALIDATION = True

# RULE: ENSURE FROM LANGUAGE CHARACTER MATCH
# NOTE: This rule will ensure the from language only contains characters defined in the VALID_TO_CHARS_PATTERN
ENABLE_RULE_TO_LANGUAGE_VALIDATION = True

def LogLine(input:str):
    with open(file=LOG_OUTPUT_FILE, mode="a", encoding="utf-8") as f:
        f.write(input)

def cleanse_repeating_punctuation(input:str):
    '''applies rule to cleanse repeating punctuation'''
    # IF THE INPUT WAS CLEARED OR IS EMPTY, FALL OUT
    if input == "":
        return input

    repeating_punctuation = REPEATING_PUNCTUATION_PATTERN.search(input)

    if repeating_punctuation:
        last_char = repeating_punctuation.group(0)[0]
        cleansed = input.replace(repeating_punctuation.group(0), last_char)
        input = cleansed

    return input

def cleanse_grouped_punctuation(input:str):
    # IF THE INPUT WAS CLEARED OR IS EMPTY, FALL OUT
    if input == "":
        return input

    grouped_punctuation = GROUPED_PUNCTUATION_PATTERN.search(input)
    
    if grouped_punctuation:
        last_char = grouped_punctuation.group(0)[0]
        cleansed = input.replace(grouped_punctuation.group(0), last_char)
        input = cleansed    

    return input
    
def cleanse_malformed_punctuation(input:str):
    # IF THE INPUT WAS CLEARED OR IS EMPTY, FALL OUT
    if input == "":
        return input

    malformed_punctuation = MALFORMED_PUNCTUATION_PATTERN.search(input)
    punct = {".", "?", "!"}
    
    if malformed_punctuation:
        LogLine(f"invalid_punctuation\t{input}\n")
        input = ""        

    if len(input) > 0 and input[-1] not in punct:
        LogLine(f"no_punctuation\t{input}\n")
        input = ""        

    return input

def remove_unicode_characters(input):
    # IF THE INPUT WAS CLEARED OR IS EMPTY, FALL OUT
    if input == "":
        return input

    # this routine cleans common unicode characters found in some of the example data, extend, reduce or disable this rule as needed.
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

def cleanse_language_start(input:str, pattern: Pattern[str]):
    '''drops the sentence if it starts with an invalid character'''
    # IF THE INPUT WAS CLEARED OR IS EMPTY, FALL OUT
    if input == "":
        return input

    # if the sentence does not start with valid chars, eject it from training set
    if not re.match(pattern, input):
        LogLine(f"invalid_start_chars_pattern\t{input}\n")
        return ""
        
    return input

def cleanse_language_invalid_characters(input:str, pattern: Pattern[str]):
    '''drops the sentence if it contains an invalid character'''
    # IF THE INPUT WAS CLEARED OR IS EMPTY, FALL OUT
    if input == "":
        return input
    
    # if we do not match, then drop the sentence
    if not re.match(pattern, input):
        LogLine(f"invalid_chars_pattern\t{input}\n")
        return ""
    
    return input

def cleanse_align_punctuation(from_lang: str, to_lang:str):
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
        reserve_from_lang = parts[FROM_LANGUAGE_INDEX]
        reserve_to_lang = parts[TO_LANGUAGE_INDEX]

        from_lang = parts[FROM_LANGUAGE_INDEX]
        to_lang = parts[TO_LANGUAGE_INDEX]

        # encode as utf-8    
        from_lang_bytes = from_lang.encode('utf-8')
        to_lang_bytes = to_lang.encode('utf-8')      

        from_lang = from_lang_bytes.decode('utf-8').strip()
        to_lang = to_lang_bytes.decode('utf-8').strip()

        # FROM LANG RULES
        if ENABLE_RULE_REMOVE_UNICODE_FROM_LANG:
            from_lang = remove_unicode_characters(from_lang)

        if ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_FROM_LANG:
            from_lang = cleanse_repeating_punctuation(from_lang)

        if ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_FROM_LANG:
            from_lang = cleanse_grouped_punctuation(from_lang)

        if ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_FROM_LANG:
            from_lang = cleanse_malformed_punctuation(from_lang)
        
        if ENABLE_RULE_FROM_LANGUAGE_START_VALIDATION:
            from_lang = cleanse_language_start(from_lang, VALID_FROM_START_CHARS_PATTERN)
        
        if ENABLE_RULE_FROM_LANGUAGE_VALIDATION:
            from_lang = cleanse_language_invalid_characters(from_lang, VALID_FROM_CHARS_PATTERN)

        # TO LANG RULES
        if ENABLE_RULE_REMOVE_UNICODE_TO_LANG:
            to_lang = remove_unicode_characters(to_lang)       

        if ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_TO_LANG:
            to_lang = cleanse_repeating_punctuation(to_lang)       
        
        if ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_TO_LANG:
            to_lang = cleanse_grouped_punctuation(to_lang)       

        if ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_TO_LANG:
            to_lang = cleanse_malformed_punctuation(to_lang)

        if ENABLE_RULE_TO_LANGUAGE_START_VALIDATION:
            to_lang = cleanse_language_start(to_lang, VALID_TO_START_CHARS_PATTERN)
        
        if ENABLE_RULE_TO_LANGUAGE_VALIDATION:
            to_lang = cleanse_language_invalid_characters(to_lang, VALID_TO_CHARS_PATTERN)

        # LANGUAGE AGNOSTIC RULES
        if ENABLE_RULE_ALIGN_PUNCTUATION:
            lang_parts = cleanse_align_punctuation(from_lang, to_lang)
            from_lang = lang_parts[0]
            to_lang = lang_parts[1]

        if ENABLE_RULE_ALIGN_START:
            lang_parts = cleanse_align_starts(from_lang, to_lang)
            from_lang = lang_parts[0]
            to_lang = lang_parts[1]
                        
        if from_lang == "" or to_lang == "":
            text = ""
        else:
            text = f"{from_lang}\t{to_lang}"
            
            if ENABLE_RULE_LOWERCASE:
                text = text.lower()

        return text
    LogLine(f"unable to split by delimiter\t\n")
    return "" # drop rule hit invalid delimiter split

def clean_dataset(file: str) -> str:
    
    print(f'Working on file {file}')

    """Cleans a Tab seperated dataset for training purposes"""
    file_path = Path(f"{DATA_FOLDER}/").resolve().joinpath(file)

    file = Path(file_path)

    output_dir = Path(f"{OUTPUT_FOLDER}/").resolve()
    
    new_file = output_dir / f"{file.stem}_Cleansed.txt"
    
    lines = file.read_text(encoding="utf-8").strip().split("\n")

    new_lines = []
    new_lower_compressed_lines = []
    for line in lines:
        if ENABLE_RULE_DEDUPLICATION:
            new_line = clean_line(line)
            if new_line.strip() != "":
                lower = new_line.lower().replace(" ", "") # let's deduplicate by lowered, but keep case
                if lower not in new_lower_compressed_lines:
                    new_lower_compressed_lines.append(lower)
                    new_lines.append(new_line)
                else:
                    LogLine(f"dropped duplicate\t{new_line}\n")
        else:
            new_line = clean_line(line)
            new_lines.append(new_line)

    text = "\n".join(new_lines)

    new_file.write_text(text, encoding="utf-8")
    
    print(f'Completed File {file}')

    return new_file

def file_read_Task(file:str):
    clean_dataset(file)

def rules_report():
    print('SCRIPT IS EXECUTING WITH THE FOLLOWING RULES CONFIGURATION')
    print(f'ENABLE_RULE_DEDUPLICATION: {ENABLE_RULE_DEDUPLICATION}')
    print(f'ENABLE_RULE_LOWERCASE: {ENABLE_RULE_LOWERCASE}')
    print(f'ENABLE_RULE_REMOVE_UNICODE_FROM_LANG: {ENABLE_RULE_REMOVE_UNICODE_FROM_LANG}')
    print(f'ENABLE_RULE_REMOVE_UNICODE_TO_LANG: {ENABLE_RULE_REMOVE_UNICODE_TO_LANG}')
    print(f'ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_FROM_LANG: {ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_FROM_LANG}')
    print(f'ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_TO_LANG: {ENABLE_RULE_CLEAN_REPEATING_PUNCTUATION_TO_LANG}')
    print(f'ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_FROM_LANG: {ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_FROM_LANG}')
    print(f'ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_TO_LANG: {ENABLE_RULE_CLEAN_GROUPED_PUNCTUATION_TO_LANG}')
    print(f'ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_FROM_LANG: {ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_FROM_LANG}')
    print(f'ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_TO_LANG: {ENABLE_RULE_CLEAN_MALFORMED_PUNCTUATION_TO_LANG}')
    print(f'ENABLE_RULE_ALIGN_PUNCTUATION: {ENABLE_RULE_ALIGN_PUNCTUATION}')
    print(f'ENABLE_RULE_ALIGN_START: {ENABLE_RULE_ALIGN_START}')
    print(f'ENABLE_RULE_FROM_LANGUAGE_START_VALIDATION: {ENABLE_RULE_FROM_LANGUAGE_START_VALIDATION}')
    print(f'ENABLE_RULE_TO_LANGUAGE_START_VALIDATION: {ENABLE_RULE_TO_LANGUAGE_START_VALIDATION}')
    print(f'ENABLE_RULE_FROM_LANGUAGE_VALIDATION: {ENABLE_RULE_FROM_LANGUAGE_VALIDATION}')
    print(f'ENABLE_RULE_TO_LANGUAGE_VALIDATION: {ENABLE_RULE_TO_LANGUAGE_VALIDATION}')

def parallel_clean():
    LogLine(f"Main\tProcess Starting\tfile cleanse\t{DATA_FOLDER}\n")
    
    #parallel process files in batches of 20
    training_files = os.listdir(DATA_FOLDER)
    
    with multiprocessing.Pool(MAX_PARALLELISM) as pool:
        pool.map(clean_dataset, training_files)

if __name__ == "__main__":
    rules_report()
    parallel_clean()