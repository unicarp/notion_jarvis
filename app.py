"""
Notion AI Task Orchestrator - Main Application Entry Point

This script ties together the Groq NLP extracition module and the
Notion API Client. It takes user input, processes it into structured
tasks, and batches the upload to the target Notion database.
"""

from main import orchestrate_tasks
from notion_client import create_notion_task

def main():
    print("---Task Orchestrator Initiated---")

    # Capture the brain dump
    user_input = input("\n[Jarvis]: What's on your mind today?\n>")
    
    if not user_input.strip():
        print("[Jarvis]: No input detected. Shutting down...")
        return

    # Process with LLM
    print("\n---Processing language and structuring taks...---")
    try:
        tasks = orchestrate_tasks(user_input)
    except Exception as e:
        print(f"\nX---CRITICAL: Failed to process tasks with LLM. Error: {e}")
        return
    
    if not tasks:
        print("[Jarvis]: No actionable tasks detected in the input.")
        return

    # Batch processing to Notion
    print(f"\n---Extracted {len(tasks)} tasks. Pushing to Notion...")
    print("="*50)

    succes_count = 0
    for task in tasks:
        # We use the function imported from notion_client.py
        is_success = create_notion_task(task)
        if is_success:
            succes_count += 1
    
    print("-"*50)
    print(f"O---Workflow Completed: {succes_count}/{len(tasks)} tasks synced succesfully.")
    print("="*50)

if __name__ == "__main__":
    main()
