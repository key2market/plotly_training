import json
from openai_client import OpenAI
import plotly.graph_objects as go
import uuid
import time
import functions as f

openai_inst = OpenAI('creds.ini')
# Define the filename where you want to write
manifest = 'manifest.csv'


def get_generated_questions():
    # Initialize an empty list to hold the 'value1' values
    q_list = []

    # Open the file in read mode ('r')
    with open(manifest, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Split the line into a list using the comma as a delimiter
            values = line.strip().split(',')
            # Append the first value (value1) to the list
            # Assuming that each line has at least one comma and two values
            q_list.append(values[0])

    return q_list

def record_question(analyst_question, run_id):
    # Open the file in write mode ('w') which will create the file if it doesn't exist
    with open(manifest, 'a') as file:
        # Write the two values as a comma-separated line of text to the file
        file.write(f"{analyst_question},{run_id}\n")

# Loop with 50 iterations
for i in range(50):
    print(f"Step {i+1}")

    # Generate a UUID and convert to a string
    unique_id = str(uuid.uuid4())

    # Get the current time in seconds since the Epoch
    timestamp = time.time()
    # Combine the UUID and timestamp to create a unique microstamp
    run_id = f"{unique_id}-{timestamp}"

    openai_inst.reset_conversation()

    # start
    generated_qs = get_generated_questions()
    prompt = f.load_prompts("prompts", "generate_question.txt", ','.join(generated_qs), "context.txt")
    #print(prompt)

    #Generate Analyst question
    analyst_question = openai_inst.get_chat_response("gpt-4", prompt, False)
    print(analyst_question)

    #Generate SQL Query
    openai_inst.reset_conversation()
    prompt = f.load_prompts("prompts", "sql.txt", "context.txt")
    response_sql = openai_inst.get_chat_response("gpt-4", prompt, True)

    # Extract SQL
    query = f.extract_text_between_markers(response_sql, "SQL")
    print(query)

    # Run SQL Query
    result = f.run_query(query)
    print(result)
    if result == "ERROR":
        record_question(analyst_question, run_id)
        continue

    #Generate Plotly sql
    prompt = f.load_prompts("prompts", "plotly.txt", '\n'.join(str(tup) for tup in result) )
    response_plotly = openai_inst.get_chat_response("gpt-3.5-turbo", prompt, True)
    #print(response_plotly)
    plotly = f.extract_text_between_markers(response_plotly, "PLOTLY")

    #Generate Plotly sql
    # Data and layout specifications
    """
    data = [
        {"x": ["Shows", "Sports", "Concerts"], "y": [1500, 2000, 1000], "type": "bar"}
    ]
    layout = {
        "title": "Total Tickets Sold by Event Category",
        "xaxis": {"title": "Event Category"},
        "yaxis": {"title": "# of Tickets Sold"}
    }
    """
    print(plotly)
    # Convert JSON string to Python dictionary
    chart_data = json.loads(plotly)

    # Create the figure with the specified data and layout
    fig = go.Figure(data=chart_data['data'], layout=chart_data['layout'])

    # Save the figure as an image
    fig.write_image(f"images/{run_id}.png")

    record_question(analyst_question, run_id )

    # Create a dictionary with the text variables
    data = {
        "run_id": run_id,
        "question": analyst_question,
        "sql": query,
        "plotly_code": plotly,
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)

    # If you want to write the JSON to a file
    with open(f"json/{run_id}.json", 'w') as json_file:
        json_file.write(json_data)