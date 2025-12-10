# Temporal + OpenAI Agents Plugin

This project demonstrates how to **durably orchestrate an OpenAI Agent** using Temporal. 

Instead of writing a manual multi-step workflow, we use the **`temporalio.contrib.openai_agents`** plugin to deploy a single Autonomous Agent (`CityGuideAgent`) that automatically calls Temporal Activities as "Tools".

## Key Concepts

1.  **Durable Agent**: The Agent's "Model Context" (chat history) is preserved durably. If the worker crashes mid-conversation, it resumes exactly where it left off.
2.  **Activities as Tools**: We simply pass our Temporal Activities (`get_weather`) to the Agent logic. The SDK automatically converts them into OpenAI function definitions.
3.  **Human-in-the-Loop (Implicit)**: Because every tool call is a Temporal Activity, you get automatic retries, timeouts, and visibility for every single action the AI takes.

## Project Structure

- **`workflows.py`**: Defines `CityGuideAgent`. It initializes an `Agent` with specific instructions and tools, then passes control to `Runner.run()`.
- **`activities.py`**: Defines the "Tools". 
    - `get_weather`: Simulates a weather API (using a sub-agent).
    - `lookup_local_activities`: Simulates a local event search (using a sub-agent).
- **`worker.py`**: Connects to Temporal with the `OpenAIAgentsPlugin` enabled and hosts the workflow/activities.
- **`starter.py`**: Starts the `CityGuideAgent` workflow for a specific city.

## Prerequisites

- Python 3.10+
- [Temporal CLI](https://docs.temporal.io/cli) installed.
- OpenAI API Key.

## How to Run

1.  **Start Temporal Server**
    ```bash
    temporal server start-dev
    ```

2.  **Install Dependencies**
    ```bash
    # Ensure you have the agent SDK installed (adjust version if needed)
    pip install temporalio openai-agents
    ```

3.  **Start the Worker**
    ```bash
    export OPENAI_API_KEY="sk-..."
    python worker.py
    ```

4.  **Run the Agent**
    ```bash
    python starter.py "Paris"
    ```

## What Happens?

1.  The Workflow starts the **City Guide Agent**.
2.  The Agent thinks: *"I need to check the weather in Paris first."*
3.  It calls the `get_weather` tool.
    - **Temporal executes `get_weather` as an Activity.**
4.  The Activity returns "55F and Rainy".
5.  The Agent thinks: *"Okay, it's rainy. I should look for indoor activities."*
6.  It calls the `lookup_local_activities` tool with context "indoor".
    - **Temporal executes `lookup_local_activities`.**
7.  The Agent receives the list and writes the final itinerary.
8.  The workflow completes and returns the guide.

## Visibility

Navigate to [http://localhost:8233](http://localhost:8233) to see the Agent in action! You will see the Workflow Execution `CityGuideAgent` and the individual Activity executions for every tool call it made.
