# AI-Powered-personal-Assistant# AI-Powered Personal Task Assistant

A tool that uses AI to manage tasks by parsing natural language input, prioritizing tasks, and providing user insights.

## Features
- Parse tasks from text (e.g., "Write code by tomorrow").
- Prioritize tasks based on deadlines.
- Store tasks in a lightweight SQLite database.
- (In progress: Insights on user habits, web UI with Streamlit)

## Tech Stack
- **Python**: Core language
- **spaCy**: Natural language processing
- **scikit-learn**: Task prioritization
- **SQLite**: Task storage

## Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/task-assistant.git
   cd task-assistant
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python src/main.py
