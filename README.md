# Blackboard-Based LLM Agents MVP

A minimal multi-agent system where LLM-based agents collaborate through a shared in-memory blackboard to perform article-related tasks.

## Features

- **Blackboard**: Shared message board for agent communication
- **LLM Agents**: Writer, Editor, and Grammar agents with specialized prompts
- **Smart Routing**: Configurable context window for agent decision-making
- **Real-time CLI**: Interactive interface with live message display

## Architecture

### Components

1. **Blackboard** (`blackboard.py`)
   - Stores messages with ID, sender, text, and timestamp
   - Provides methods to retrieve messages by count or ID

2. **Router** (`router.py`) 
   - Manages context window (default: last 1 message)
   - Tracks processed messages to avoid duplication
   - Formats context for agent decision-making

3. **Agents** (`agents.py`)
   - **WriterAgent**: Creates article drafts and written content
   - **EditorAgent**: Improves writing style and structure  
   - **GrammarAgent**: Fixes grammar and language errors
   - Each agent uses LLM calls to decide whether to act and how to process text

4. **Main System** (`main.py`)
   - CLI interface for user interaction
   - Background thread for agent processing
   - Real-time message display with color coding

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
1.1. **Create a virtual environment**:
   ```bash
   python3 -m venv myenv
   source .venv/bin/activate # On Windows: myenv\Scripts\activate
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. Run the system:
   ```bash
   python main.py
   ```

## Example Workflow

1. **User**: "Write a short draft about collaborative AI agents."
2. **WriterAgent**: Detects writing request → generates draft → posts to blackboard
3. **EditorAgent**: Sees draft → improves style → posts improved version
4. **GrammarAgent**: Sees text → fixes any grammar issues → posts final version

## Usage

- Type requests in natural language
- Agents automatically decide whether to act based on their goals
- View real-time collaboration on the blackboard
- Type `quit` or `exit` to stop

## Configuration

- Modify `context_window` in `main.py` to change how many messages agents consider
- Adjust agent prompts in `agents.py` for different behaviors
- Add new agent types by extending `BaseAgent`
