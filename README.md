
# README for the Git Repository

## Introduction
This repository contains scripts for generating synthetic training data based on a data structure schema of a database. 
This repository leverages AI to create questions about the data, executes SQL queries, and generates visualizations using Plotly.

The following training data is generated (in order of creation):
1. A question about data Ex "How much sales did I have last year?"
2. An SQL to answer the question
3. A Plotly JSON to visualise data returned by the SQL
4. A screenshot of Plotly Image for visual inspection

## Contents
1. `functions.py` - Contains utility functions.
2. `openai_client.py` - Manages interactions with the OpenAI API.
3. `run.py` - The main script that orchestrates the process of generating questions, executing SQL, and creating visualizations.
4. `requirements.txt` - Lists the necessary Python packages.

## Setup Instructions

### Creating a Virtual Environment
1. Ensure Python 3 is installed on your system.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On Unix or MacOS: `source venv/bin/activate`

### Installing Dependencies
1. With the virtual environment activated, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. Update the `creds.ini` file with your OpenAI API key.
2. Ensure you have a PostgreSQL database set up as the script uses `psycopg2`.
3. Run the `run.py` script:
   ```bash
   python run.py
   ```
This script performs the following actions:
- Connects to the OpenAI API to generate questions about the data. Schema of the data is provided from the schema file `context.txt`.
- Connects to the OpenAI API to generate SQL query from the schema and the question.
- Executes SQL query.
- Connects to the OpenAI API with the data from the query and asks AI to create the [Plotly](https://plotly.com/) json. 
- Uses Plotly to create visualizations from the SQL query results.

## File storage
- `manifest.csv` here we record all of the questions generated and the RUN ID during which they were generated. It is important not to repeat a questions so here we keep track.
- `images/` in this directory we save the generated plotly images for visual inspection of which images are good or not
- `json/` here we store the AI generated plotly JSON files

## Important Notes
- Ensure that the PostgreSQL database credentials are correctly set in the `config.ini` file.
- The scripts expect certain structures and formats in the data. Please refer to the script comments for detailed information.

