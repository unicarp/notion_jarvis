# Notion AI Task Orchestrator
### A.K.A. "Notion Jarvis"

## Overview
An LLM-powered automation tool designed to eliminate decision fatigue by converting unstructured natural language (brain dumps) into structured, prioritized tasks directly within a Notion database.

This project serves as a lightweight, low-friction pipeline fo manage daily workflows, allowing for maximum focus on deepwork and complex daily or non-daily tasks.

## Tech-Stack
- **Core** : Python 3.10.X
- **LLM Engines** : Groq Llama 3 (Testing/Deploy)
- **Integrations** : Notion API
- **Environment Management** : Conda

## Local Setup
Make sure to have already installed any Conda or Miniconda Version. You can install Miniconda here: https://www.anaconda.com/download

### 1. Clone the repository
```
git clone [https://github.com/unicarp/notion_jarvis.git](https://github.com/unicarp/notion_jarvis.git)
cd notion_jarvis
```

### 2. Environment Configuration
Create and activate the isolated Conda environmentto ensure dependency stability:

```
conda create -n notion_jarvis python=3.10.13
conda activate notion_jarvis
pip install -r requirements.txt
```
### 3. Environment Variables
Create a `.env` file in the project's root directory (it is highly recommended to add it to your `.gitignore` file) and configure your API keys:

```
GROQ_API_KEY="your_groq_api_key"
NOTION_DATABASE_ID="your_notion_target_database_id"
NOTION_API_KEY="your_notion_internal_integration_token"
```

## Current Status
**In Development:** Version 1.0 (MVP). Setting up the initial NLP extraction pipeline and API handshake with Notion.