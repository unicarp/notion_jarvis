"""
Notion AI Task Orchestrator - Notion API Client

This module handles the HTTP communication with the Notion API.
It formats the extracted JSON tasks into Notion's specific block structure
and pushes them to the target database.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NOTION_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Standard headers required by Notion API
HEADERS = {
    "Authorization" : f"Bearer {NOTION_KEY}",
    "Content-Type" : "application/json",
    "Notion-Version" : "2022-06-28"
}

def create_notion_task(task_data):
    """
    Send a single task to the Notion database.

    Args:
        task_data (dict): A dictionary containing 'task', 'priority', and 'due_date'.
    
    Returns:
        bool: True if succesful, False otherwise.
    """
    url = "https://api.notion.com/v1/pages"

    # Structure the mandatory fields (Title and Select)
    payload = {
        "parent" : {"database_id": DATABASE_ID},
        "properties" : {
            "Tarea" : {
                "title" : [
                    {
                        "text" : {
                            "content" : task_data["task"]
                        }
                    }
                ]
            },
            "Prioridad" : {
                "select" : {
                    "name": task_data["priority"]
                }
            }
        }
    }

    # Add the Date ONLY if it's not null (Notion throws an error for a 'null' Date)
    if task_data.get("due_date"):
        payload["properties"]["Fecha Límite"] = {
            "date" : {
                "start" : task_data["due_date"]
            }
        }
    
    # Make the HTTP POST request
    try:
        response = requests.post(url, headers=HEADERS, json=payload)

        # Raise an exception if the request failed
        response.raise_for_status()
        print(f"O - Task created successfully: {task_data['task']}")
        return True
    except requests.exceptions.HTTPError as err:
        print(f"X - Error sending task to Notion: {err}")
        print("Notion details:", response.text)
        return False

# ---Test Block---
if __name__ == "__main__":
    print("--- Test: Sending Dummy Task to Notion ---")

    # Fake task to test the connection safely
    dummy = {
        "task" : "Test de conexión para el Notion Jarvis",
        "priority" : "Alta",
        "due_date" : "2026-12-31"
    }

    create_notion_task(dummy)
