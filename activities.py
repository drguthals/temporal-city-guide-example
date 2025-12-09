import os
import asyncio
from temporalio import activity
from openai import AsyncOpenAI
from agents import Agent, Runner
# Import the WebSearchTool provided by the openai-agents library. 
# This tool allows the agent to perform real-time internet searches.
from agents.tool import WebSearchTool

# ----------------------------------------------------------------------------
# Temporal Activity: Get Weather
# ----------------------------------------------------------------------------
@activity.defn
async def get_weather(city: str) -> str:
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    """
    Activity to fetch the current weather using an AI Agent with web search capabilities.
    """
    activity.logger.info(f"Getting weather for: {city}")
    
    # Internal function to run the agent synchronously.
    # We define it here to isolate the Agent instantiation and execution.
    def _run_agent():
        agent = Agent(
            name="Weather Reporter",
            instructions="You are a weather reporter. Use the web search tool to find the current date and provide "
            "the current weather and temperature in Fahrenheit for the given city for today's date. Be concise.",
            tools=[WebSearchTool()],
        )
        # Runner.run_sync executes the agent loop (Thought -> Action -> Observation) until completion.
        result = Runner.run_sync(agent, f"City: {city}")
        return result.final_output.strip()

    # CRITICAL: We run the synchronous blocking agent code in a separate thread 
    # using asyncio.to_thread. This prevents blocking the Temporal activity heartbeat 
    # and allows other async duties to proceed.
    return await asyncio.to_thread(_run_agent)

# ----------------------------------------------------------------------------
# Temporal Activity: Get Activity Recommendation
# ----------------------------------------------------------------------------
@activity.defn
async def get_activity(city: str, weather: str) -> str:
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    """
    Activity to suggest a travel activity based on the city and current weather.
    """
    activity.logger.info(f"Finding activity for {city} with weather: {weather}")

    def _run_agent():
        agent = Agent(
            name="Activity Finder",
            instructions="You are a travel guide. Use the web search tool to find one interesting activity to do in "
            "the city based on the weather. Be concise.",
            tools=[WebSearchTool()],
        )
        result = Runner.run_sync(agent, f"City: {city}, Weather: {weather}")
        return result.final_output.strip()

    return await asyncio.to_thread(_run_agent)

# ----------------------------------------------------------------------------
# Temporal Activity: Create Guide
# ----------------------------------------------------------------------------
@activity.defn
async def create_guide(city: str, weather: str, activity_text: str) -> str:
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    """
    Activity to synthesize the weather and activity into a final formatted guide.
    It also handles unit conversion (Fahrenheit <-> Celsius) based on the locale.
    """
    activity.logger.info(f"Creating guide for {city}")

    def _run_agent():
        agent = Agent(
            name="Guide Creator",
            instructions="You are a helpful travel assistant. Determine if the city typically uses Celsius, if so convert the temperature "
            "in the weather description to Celsius. Only include either Fahrenheit or Celsius in the final output, "
            "depending on what the city typically uses. Then combine the weather and activity into a short, friendly guide for the user."
        )
        
        result = Runner.run_sync(
            agent, f"City: {city}\nWeather (F): {weather}\nActivity: {activity_text}"
        )
        return result.final_output.strip()

    return await asyncio.to_thread(_run_agent)
