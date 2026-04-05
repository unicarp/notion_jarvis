"""
Notion AI Task Orchestrator - Telegram Interface

This module acts as the entry point for the Telegram bot,
routing voice inputs through the audio service, the task orchestrator,
and finally to the Notion API client.
"""

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Local modules import
from audio_service import transcribe_audio
from main import orchestrate_tasks
from notion_client import create_notion_task

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID", 0))

def isValidUser(update):
    """
    Validates authorized users
    """
    return update.effective_user.id == TELEGRAM_USER_ID

async def start(update:Update, context):
    """
    Handle the /start command.
    
    Initializes the conversation with the user and confirms that the
    system is online and ready to receive multimodal inputs.
    """
    if not isValidUser(update):
        return

    await update.message.reply_text("[Jarvis]: System online. Awaiting input.")

async def process_and_upload(update, text):
    """
    Core logic to process text and push to Notion.
    
    Args:
        update: The Telegram update object containing the message context.
        text (str): The transcribed voice note or direct text input.
    """

    try:
        await update.message.reply_text("Structuring tasks...")

        # Extracts tasks via LLM
        tasks = orchestrate_tasks(text)
        if not tasks:
            await update.message.reply_text("[Jarvis]: No actionable tasks detected in the input.")
            return
        
        # Upload the Notion
        success_count = 0
        for task in tasks:
            is_success = create_notion_task(task)
            if is_success:
                success_count += 1
        
        await update.message.reply_text(f"O - Workflow Completed: {success_count}/{len(tasks)} tasks synced succesfully.")
    except Exception as e:
        await update.message.reply_text(f"X - Critical Error: {e}")

async def handle_voice(update, context):
    """
    Process incoming voice messages and execute pipeline.
    """
    if not isValidUser(update):
        return

    file_path = "voice_note.ogg"

    try:
        # Download audio from Telegram
        file = await context.bot.get_file(update.message.voice.file_id)
        await file.download_to_drive(file_path)
        await update.message.reply_text("Processing audio input...")

        # Transcribe audio to text
        text = transcribe_audio(file_path)
        #  /// TESTING ONLY
        await update.message.reply_text(f"[Jarvis]: Transcribed: {text}")

        # Route to core logic
        await process_and_upload(update, text)
    
    finally:
        # Clean up local storage
        if os.path.exists(file_path):
            os.remove(file_path)

async def handle_text(update, context):
    """
    Process incoming text messages.
    """
    if not isValidUser(update):
        return

    text = update.message.text
    await process_and_upload(update,text)

def main():
    """
    Initialize and start the bot polling
    """
    print("---Telegram Bot Interface Initiated---")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    # New handler for normal text, ignoring commands like /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Listening for text and voice updates...")
    app.run_polling()

if __name__ == "__main__":
    main()
