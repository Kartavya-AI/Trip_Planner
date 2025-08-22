import os
from duckduckgo_search import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

def intent_mapper_node(state: dict) -> dict:
    """Validates required fields and sets intent."""
    print("👉 Running intent_mapper_node...")

    required_fields = ["origin", "destination", "travel_date", "days"]
    missing = [f for f in required_fields if f not in state or not state[f]]

    if missing:
        state["errors"] = f"Missing fields: {missing}"
    state["intent"] = "road_trip_plan"
    return state


def finder_node(state: dict) -> dict:
    """Suggests stops, food, and attractions on the route."""
    print("👉 Running finder_node...")

    origin = state["origin"]
    destination = state["destination"]
    travel_date = state["travel_date"]
    days = state["days"]
    interests = state.get("interests", "general sightseeing and leisure")
    dietary = state.get("dietary_preferences", "no specific preference")
    food_budget = state.get("food_budget", "flexible")

    # 🔎 DuckDuckGo live search
    search_query = f"Best scenic stops, attractions, and restaurants between {origin} and {destination} road trip"
    search_results = list(DDGS().text(search_query, max_results=5))
    formatted_results = "\n".join(
        [f"- [{r['title']}]({r['href']}) - {r['body']}" for r in search_results]
    )

    prompt = f"""
    Plan a road trip from {origin} to {destination} starting {travel_date} for {days} days.
    Traveler interests: {interests}.
    Food preferences: {dietary}, food budget: {food_budget}.

    Use these search results as grounding:
    {formatted_results}

    Suggest:
    - Scenic halts or towns on the way
    - Good food options (restaurants, dhabas)
    - Interesting activities between {origin} and {destination}
    """

    response = llm.invoke(prompt)
    state["finder_results"] = response.content
    state["user_selected_stay"] = True  # to trigger itinerary
    return state


def itinerary_node(state: dict) -> dict:
    """Generates complete day-by-day itinerary with timings, activities, food, and accommodation recommendations."""
    print("👉 Running itinerary_node...")

    origin = state["origin"]
    destination = state["destination"]
    travel_date = state["travel_date"]
    days = state["days"]
    interests = state.get("interests") or "Not specified (default: general sightseeing & leisure)"
    acc_budget = state.get("accommodation_budget") or "Not specified (default: budget-friendly)"
    dietary = state.get("dietary_preferences") or "Not specified (default: no preference)"
    food_budget = state.get("food_budget") or "Not specified (default: medium-level budget)"


    prompt = f"""
    You are a professional travel planner.  

    First, summarize the **Traveler Preferences** clearly:
    - Interests: {interests}
    - Accommodation Budget: {acc_budget}
    - Dietary Preferences: {dietary}
    - Food Budget: {food_budget}

    Then, create a detailed {days}-day road trip itinerary from {origin} to {destination},
    starting on {travel_date}.  

    ⚠️ IMPORTANT: The itinerary **must be formatted as a single Markdown table only**.  
    No text, no bullet points outside the table.  

    The table should have the following columns:
    | Day | Time | Activity / Place | Food & Dining | Accommodation & Travel Tips |


    Rules:
    - Every day must be fully represented in the table.  
    - Each row = one activity/time slot.  
    - End every day with a **Hotel Recommendation row**.  
    - Do not include any notes outside the table. 
        For EACH day, provide a timeline with:

    Example (shortened):

    | Day | Time | Activity / Place | Food & Dining | Accommodation & Travel Tips |
    |-----|------|------------------|---------------|-----------------------------|
    | Day 1 (2025-08-23): Origin → Destination | 7:00 AM | Depart from Origin | Breakfast at roadside dhaba | Carry water & snacks |
    | Day 1 (2025-08-23): Origin → Destination | 8:00 PM | Dinner at local restaurant | Try local thali | Hotel Recommendation: XYZ Hotel |

    Now generate the full {days}-day itinerary in this format.
    """

    response = llm.invoke(prompt)
    state["itinerary"] = response.content
    return state
