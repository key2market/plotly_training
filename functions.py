import psycopg2
import configparser
import os
import re

def is_filename(string):
    # Regular expression to check for valid filename characters
    # This pattern may need to be adjusted depending on the operating system and file system
    if not re.match(r'^[\w,\s-]+\.[A-Za-z]{1,4}$', string):
        return False

    # Check for illegal characters in filenames (for Windows)
    # For UNIX/Linux, you might only check for '/'
    if any(char in string for char in '<>:"/\|?*'):
        return False

    # Optionally, check if the length is more than OS allows for file names
    if len(string) > 255 or len(string) <= 1:
        return False

    return True

"""
Load text prompt from a file
Safely formats a string using str.format method.
Missing positional and keyword arguments are replaced with empty strings.
"""
def load_prompts (dir, template_name, *args):

    # Open the file in read mode and read the content
    file_path = f"{dir}/{template_name}"
    #print(f"loading file {file_path}")
    with open(file_path, 'r') as file:
        template = file.read()

    # Handling additional positional arguments
    safe_args = []

    for arg in args:

        if not is_filename(arg):
            safe_args.append(arg)
            continue

        try:
            file_path = f"{dir}/{arg}"
            #print(f"loading file {file_path}")
            with open(file_path, 'r') as file:
                # Read the content of each file and add to safe_args
                safe_args.append(file.read().strip())
        except FileNotFoundError:
            print(f"Warning: File '{file_path}' not found, loading it as text")
            safe_args.append(arg)

    # Adjust the number of arguments to match the number of placeholders
    placeholders_count = template.count('{}')
    safe_args += [''] * (placeholders_count - len(safe_args))

    # Format the template with the contents from the files
    return template.format(*safe_args)

def extract_text_between_markers(text, type):
    type = type.upper()
    marker_start = f"{type}__START"
    marker_end = f"{type}__END"

    # Find the start and end indices of the markers
    start_index = text.find(marker_start)
    end_index = text.find(marker_end)

    # Check if both markers are found
    if start_index != -1 and end_index != -1:
        # Adjust start index to the end of the start marker
        start_index += len(marker_start)

        # Extract the text between the markers
        extracted_text = text[start_index:end_index].strip()
        return extracted_text
    else:
        return False

def read_db_config(filename='creds.ini', section='redshift'):
    # Create a parser
    parser = configparser.ConfigParser()
    # Read the configuration file
    parser.read(filename)

    # Get the section
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file.')

    return db


def run_query(query):
    try:
        # Read the database configuration
        params = read_db_config()

        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()

        # Execute a query
        cur.execute(query)

        # Fetch the result
        result = cur.fetchall()

        # Close the cursor and connection
        cur.close()
        conn.close()

        return result

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "ERROR"
