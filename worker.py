import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
from workflows import CityGuideAgent
from activities import get_weather, lookup_local_activities

async def main():
    # CONNECT WITH THE PLUGIN
    # This enables the "Model Context Durability" (saving chat history)
    client = await Client.connect("localhost:7233", plugins=[OpenAIAgentsPlugin()])

    worker = Worker(
        client,
        task_queue="city-guide-queue",
        workflows=[CityGuideAgent],
        activities=[get_weather, lookup_local_activities]
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())