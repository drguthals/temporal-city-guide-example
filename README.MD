# City Guide Workflow

This project demonstrates a **Temporal Workflow** that orchestrates AI Agents to generate a personalized city travel guide.

It is designed as a durable, scalable Temporal application. Instead of running as a single script, each step of the process is an independent Activity that can be retried, timed out, or scaled independently. This is based on the Tensorlake quickstart on the tensorlakeai/tensorlake repo.

## Overview

The workflow coordinates three distinct steps (Activities):
1.  **Get Weather**: An AI Agent uses a web search tool to find the current weather for a given city.
2.  **Get Activity**: An AI Agent suggests an activity based on the retrieved weather.
3.  **Create Guide**: An AI Agent synthesizes the information into a friendly, formatted guide, converting temperature units if necessary.

## Prerequisites

- **Python 3.10+**
- **Temporal CLI** (to run the dev server)
  ```bash
  brew install temporal
  ```
- **OpenAI API Key** (set as an environment variable)
  ```bash
  export OPENAI_API_KEY="sk-..."
  ```
- **Dependencies**
  ```bash
  pip install temporalio openai-agents
  ```

## Project Structure

- `activities.py`: Defines the Temporal Activities. Each activity wraps an AI Agent (from `openai-agents`) that performs a specific task using a Web Search tool.
- `workflows.py`: Defines the Temporal Workflow (`CityGuideWorkflow`). It orchestrates the execution of the activities in a specific order.
- `worker.py`: The worker process that connects to the Temporal Server and listens for tasks (workflows and activities) to execute.
- `starter.py`: A client script that triggers the workflow execution.

## How to Run

1.  **Start the Temporal Server**
    ```bash
    temporal server start-dev
    ```
    The UI will be available at http://localhost:8233.

2.  **Start the Worker**
    Open a new terminal and run:
    ```bash
    # Ensure OPENAI_API_KEY is set
    python worker.py
    ```

3.  **Run the Workflow**
    Open another terminal and run:
    ```bash
    # You can specify a city as an argument (default is San Francisco)
    python starter.py "Tokyo, Japan"
    ```

## Example Output
```md
(venv) sarahguthals@Sarahs-MacBook-Pro-3 temporal % python3 starter.py "Milan, Italy"
Generating city guide for: Milan, Italy...

==================================================
CITY GUIDE
==================================================

Milan, Italy uses Celsius for temperature.

Today in Milan, it’s foggy with a temperature around **3 °C**, and there’s a Yellow Fog Warning in effect across Lombardy until 11:59 PM. For a cozy and inspiring escape from the mist, step inside the Museo Nazionale Scienza e Tecnologia “Leonardo da Vinci.” It’s the largest science and technology museum in Italy, packed with incredible exhibits on Leonardo’s inventions and early technologies—perfect for staying warm and entertained on a foggy day!

(venv) sarahguthals@Sarahs-MacBook-Pro-3 temporal % python3 starter.py "San Francisco"
Generating city guide for: San Francisco...

==================================================
CITY GUIDE
==================================================

San Francisco typically uses Fahrenheit for weather reports.

Here’s your friendly guide for today: With cool, partly cloudy weather in the mid- to upper-40s °F (around 46 °F currently), it’s a perfect evening to bundle up and head downtown for Let’s Glow SF—the city’s dazzling holiday projection-art festival. Enjoy the outdoor light displays on iconic buildings, sip hot chocolate, and catch some live music in the festive, crisp Bay Area air. Don’t forget to dress warmly, especially as fog may roll in later! Let me know if you need directions or tips for getting around town.
(venv) sarahguthals@Sarahs-MacBook-Pro-3 temporal % python3 starter.py
Generating city guide for: San Francisco...
```
