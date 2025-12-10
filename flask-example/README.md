# Flask City Guide Example

This directory contains a traditional (non-Temporal) implementation of the City Guide application using **Flask**. 

It is designed to demonstrate common pitfalls in building long-running AI applications with standard web servers, specifically:
- **Timeouts**: The request attempts to generate a complex itinerary with a short timeout.
- **Blocking**: The server blocks while waiting for the AI response.
- **Fragility**: If the server restarts during processing, the work is lost.

## Prerequisites

Ensure you have the necessary dependencies installed:

```bash
pip install flask openai
```

## How to Run

1.  **Set your OpenAI API Key**:
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```

2.  **Start the Server**:
    Run the Flask application (it will start on port 5001):
    ```bash
    python flask_version.py
    ```

3.  **Test the Endpoint**:
    Open a new terminal and use `curl` to request a city guide:
    
    ```bash
    curl -X POST http://localhost:5001/generate_city_guide \
         -H "Content-Type: application/json" \
         -d '{"city": "Paris, France"}'
    ```

    *Note: If the AI generation takes longer than the configured timeout (30s), this request will fail, demonstrating the fragility of the synchronous approach.*
