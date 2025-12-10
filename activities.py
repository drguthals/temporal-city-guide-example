import os
import asyncio
from temporalio import activity
from agents import Agent, Runner
from agents.tool import WebSearchTool

# ----------------------------------------------------------------------------
# Temporal Activity: Get Weather (The Tool)
# ----------------------------------------------------------------------------
@activity.defn
async def get_weather(city: str) -> str:
    """
    Get the current weather for a specific city. 
    Returns a string describing temperature and conditions.
    """
    activity.logger.info(f"Tool called: Getting weather for {city}")

    # Keep the "Sub-Agent" logic here because it's a great way 
    # to fake a Weather API without needing a real API key.
    def _run_agent():
        agent = Agent(
            name="Weather Tool",
            instructions="You are a weather API. Search for the current weather in the given city. "
            "Return ONLY the temperature and condition (e.g., '65F and Sunny'). Do not add conversational filler.",
            tools=[WebSearchTool()],
        )
        result = Runner.run_sync(agent, f"City: {city}")
        return result.final_output.strip()

    return await asyncio.to_thread(_run_agent)

# ----------------------------------------------------------------------------
# Temporal Activity: Lookup Local Activities (The Tool)
# ----------------------------------------------------------------------------
@activity.defn
async def lookup_local_activities(city: str, weather_context: str) -> str:
    """
    Find things to do in the city based on the weather context.
    """
    activity.logger.info(f"Tool called: Finding activities for {city} given {weather_context}")

    def _run_agent():
        agent = Agent(
            name="Activity Scout",
            instructions="You are a local scout. Search for 3 distinct events or places to visit "
            "based on the city and weather provided. Return them as a bulleted list.",
            tools=[WebSearchTool()],
        )
        result = Runner.run_sync(agent, f"City: {city}, Weather: {weather_context}")
        return result.final_output.strip()

    return await asyncio.to_thread(_run_agent)