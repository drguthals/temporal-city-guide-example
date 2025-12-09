import asyncio
import os
import sys
from temporalio.worker import Worker
from config import get_client
from activities import get_weather, get_activity, create_guide
from workflows import CityGuideWorkflow

async def main():
    # Ensure API key is present for the agents to function
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        # In a real deployment you might exit, but for dev we'll just warn
    
    # 1. Connect to the Temporal server acting as the task queue manager.
    client = await get_client()

    # 2. Create the Worker.
    # The worker listens to the "city-guide-task-queue".
    # It registers the Workflow (for logic) and Activities (for tasks) it can handle.
    worker = Worker(
        client,
        task_queue="city-guide-task-queue",
        workflows=[CityGuideWorkflow],
        activities=[get_weather, get_activity, create_guide],
    )

    print("City Guide Worker started... Press Ctrl+C to stop.")
    
    # 3. specific Run the worker. It will block here, polling for tasks.
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWorker stopped.")
