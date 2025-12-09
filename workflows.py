from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activities
# We use unsafe.imports_passed_through solely to allow the activity definition imports 
# to pass through the sandbox checks without issue during development.
with workflow.unsafe.imports_passed_through():
    from activities import get_weather, get_activity, create_guide

@workflow.defn
class CityGuideWorkflow:
    """
    This workflow orchestrates the creation of a city guide.
    It executes three activities sequentially:
    1. get_weather
    2. get_activity
    3. create_guide
    """
    
    @workflow.run
    async def run(self, city: str) -> str:
        # Define a Retry Policy:
        # If an activity fails (e.g., transient network issue or API error),
        # Temporal will automatically retry it up to 3 times before failing the workflow.
        retry_policy = RetryPolicy(maximum_attempts=3)
        
        # Step 1: Get Weather
        # We invoke the 'get_weather' activity. 
        # 'start_to_close_timeout' ensures the activity doesn't hang indefinitely (timeout after 30s).
        weather = await workflow.execute_activity(
            get_weather,
            city,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )

        # Step 2: Get Activity based on weather
        # The result from the previous step ('weather') is passed as input to this step.
        activity_text = await workflow.execute_activity(
            get_activity,
            args=[city, weather],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )

        # Step 3: Create Final Guide
        # This step combines the original city input and the outputs from the previous two steps.
        final_guide = await workflow.execute_activity(
            create_guide,
            args=[city, weather, activity_text],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )

        return final_guide
