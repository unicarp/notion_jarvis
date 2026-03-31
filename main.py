"""
Notion AI Task Orchestrator - Core NLP Module

This module serves as the primary natural language processing pipeline.
It leverages the Groq API (Llama 3) to process unstructured text inputs 
(brain dumps) and convert them into standardized, prioritized JSON arrays 
ready for database ingestion.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Configure the LLM
client = Groq(api_key=GROQ_KEY)

def orchestrate_tasks(user_input,*, target_language = "Spanish"):
    """
    Extracts and structures actionable tasks from unstructured text.

    This function sends a strict zero-shot prompt to the Groq API, forcing
    the LLM to return a pure JSON object. It automatically translates the 
    task descriptions into the specified target language while evaluating 
    priority based on the context provided in the raw input.

    Args:
        user_input (str): The chaotic, unstructured natural language text.
        target_language (str, optional): The desired language for the output 
            task descriptions. Defaults to "Spanish".

    Returns:
        list: A list of dictionaries containing the structured tasks. 
            Each dictionary follows the schema:
            - 'task' (str): A concise, actionable description.
            - 'priority' (str): Evaluated urgency ('High', 'Medium', 'Low').
            - 'due_date' (str | None): ISO 8601 formatted date or null.

    Raises:
        KeyError: If the 'tasks' key is missing from the API's JSON response.
        json.JSONDecodeError: If the API fails to return a valid JSON string.
    """

    prompt = f"""
    You are a professional life orchestrator.
    Analyze the following text, extract individual tasks, deadlines (ONLY if provided) and prioritize each individual task.

    CRITICAL RULES:
    1. Return ONLY a valid JSON object with a single key "tasks" containing an array of objects.
    2. Write the "tasks" description in {target_language}, regardless of the input language.
    3. Each JSON object must be strictly following this schema:
        - "task" : (string) Short, actionable description
        - "priority" : (string: "High", "Medium", "Low")
        - "due_date" : (string: "YYYY-MM-DD" or null)
    
    Input text: "{user_input}"
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output pure JSON."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type":"json_object"},
        temperature=0.1 # Low temperature = consistent, logical outputs
    )

    #Extracting the JSON content
    json_text = response.choices[0].message.content

    #Parse string into Python dictionary and returns the 'tasks' array
    return json.loads(json_text)["tasks"]

if __name__ == "__main__":
    print("---Jarvis Brain Test---")
    raw_text = "I need to finish the statistics assignment by Friday and buy groceries today"
    try:
        tasks = orchestrate_tasks(raw_text)
        print(json.dumps(tasks, indent=4))
    except Exception as e:
        print(f"Error: {e}")