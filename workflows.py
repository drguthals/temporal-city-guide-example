from datetime import timedelta
from temporalio import workflow
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
# Import the helper to convert Activities into Agent Tools
from temporalio.contrib.openai_agents.workflow import activity_as_tool
from agents import Agent, Runner # OpenAI SDK
from activities import get_weather, lookup_local_activities # Tools

@workflow.defn
class CityGuideAgent:
    @workflow.run
    async def run(self, city: str) -> str:
        # Define the Agent
        agent = Agent(
            name="City Guide",
            instructions=(
                f"You are a travel guide for {city}. "
                "1. Always check the weather first. "
                "2. Based on the weather, find appropriate activities. "
                "3. Write a final itinerary."
            ),
            tools=[
                # Wrap Activities as Tools
                # We must provide 'start_to_close_timeout' (or schedule_to_close) 
                # because these are executing as Temporal Activities.
                activity_as_tool(get_weather, start_to_close_timeout=timedelta(minutes=2)),
                activity_as_tool(lookup_local_activities, start_to_close_timeout=timedelta(minutes=2))
            ]
        )

        # Run the Agent
        # This single line replaces your 3 steps. 
        # Temporal handles the back-and-forth "Tool Call" loop durably.
        result = await Runner.run(agent, f"Plan a trip to {city}")
        return result.final_output