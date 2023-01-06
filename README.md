# Environment Setup Instructions
These scripts were written with Python 3.9.
## ANACONDA SPYDER USERS
1. Install Anaconda: https://www.anaconda.com/
2. Upgrade Conda Python Version: conda install -c anaconda python=3.9
3. Launch Spyder - Open Anaconda Navigator, Find Spyder in the list of applications and click Launch

## VS_CODE USERS
1. Install vscode: https://code.visualstudio.com/download
2. Install python 3.9: https://www.python.org/downloads/
3. Install python tools for vscode: https://code.visualstudio.com/docs/languages/python

## Install Poetry
Poetry is a package dependency management for python, this is included for easy installation of requirements and dependency auditing.
After installing python:
curl -sSL https://install.python-poetry.org | python -

### Add Poetry to Path
$HOME/.local/bin on Unix.
%APPDATA%\Python\Scripts on Windows.
$POETRY_HOME/bin if $POETRY_HOME is set.

### Install dependencies using poetry
poetry install

## Retrieve your API Token
1. Navigate to https://support.lumina247.com
2. Sign in or Signup by clicking the Profile menu
3. Copy your access token from the support site by navigating to the API ACCESS page. Paste your access token into the API_TOKEN variable at the top of the example script.
4. Install nltk library (pip install nltk)
5. Install requests library (pip install requests)
6. Run the example script.

# RCL TRANSLATION EXAMPLES
Each script provided has explicit instructions in the top of the script.

Run the scripts in this order:
data_preparation (See directory README.md for details):
    1_split.py
    2_cleanse.py
    3_combine.py
    4_deduplicate.py
    5_reverse.py

api (See directory README.md for details):
    6_train.py
    7_inference.py
    8_gleu_evaluation.py

# api
Scripts designed to work specifically with the Lumina RCL API.

## inferencehost
Scripts to control your inference host state:
1. start
2. stop
3. reboot
4. status
5. terminate

## trainingsession
Scripts to train a new model or interact with a trained model.
1. train
2. inference
3. gleu_evaluation

# data_preparation
Example scripts for cleansing bitext and tatoeba sentence pairs. 
1. split
2. cleanse
3. combine
4. deduplicate
5. reverse

# example_data
Example data sets, folder structure should always be:
- example_data/source/language
    - cleansed
    - deduplicated
    - log
    - reversed
    - split
    - test_data
    - unmodified