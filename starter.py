import asyncio
import os
import sys
from temporalio.client import Client

async def main():
    if len(sys.argv) > 1:
        city = sys.argv[1]
    else:
        city = "San Francisco"

    # 1. Connect to the Temporal Server
    client = await Client.connect("localhost:7233")

    print(f"Generating city guide for: {city}...")
    
    # 2. Start the Workflow execution.
    # 'execute_workflow' connects, starts the workflow on the server, and waits for inevitable result.
    # Ideally for long-running workflows, you would use 'start_workflow' (async) and poll/check status later.
    result = await client.execute_workflow(
        "CityGuideWorkflow",
        city,
        id=f"city-guide-{city.replace(' ', '-').lower()}", # Unique ID ensures exactly-once execution for this key
        task_queue="city-guide-task-queue",
    )

    print("\n" + "=" * 50)
    print("CITY GUIDE")
    print("=" * 50 + "\n")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
