# 🚗 Road Trip Planner

A comprehensive travel assistance application that helps users plan road trips by generating personalized itineraries, suggesting scenic stops, food options, and attractions along the route. Built with Streamlit for the user interface and FastAPI for the backend API, powered by AI (Google Gemini) and real-time search (DuckDuckGo).

## Features

- **Interactive Trip Planning Form**: Input origin, destination, travel date, number of days, and preferences (interests, budgets, dietary preferences).
- **AI-Powered Suggestions**: Uses Google Gemini LLM to generate detailed trip plans based on user preferences and real-time search results.
- **Scenic Stops & Food Options**: Recommends attractions, restaurants, and halts along the route using DuckDuckGo search.
- **Detailed Itinerary**: Generates a day-by-day itinerary in a structured Markdown table format, including timings, activities, food recommendations, and accommodation tips.
- **Dual Interface**: Available as a Streamlit web app for direct use and as a FastAPI REST API for integration.
- **Containerized Deployment**: Includes Docker support for easy deployment.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kartavya-AI/Trip_Planner.git
   cd travel_assistance
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Add your Google Gemini API key in `.env` file:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

## Usage

### Running the Streamlit Web App

To start the interactive web application:

```bash
streamlit run main.py
```

- Open your browser and navigate to `http://localhost:8501`.
- Fill in the trip details form and click "Generate Trip Plan".
- View the suggested stops and detailed itinerary.

### Using the FastAPI Backend

To run the API server:

```bash
python app.py
```

The API will be available at `http://localhost:8080`.

#### API Endpoint

- **POST /plan_trip**: Generate a trip plan.

  **Request Body** (JSON):
  ```json
  {
    "origin": "New York",
    "destination": "Los Angeles",
    "travel_date": "2023-12-01",
    "days": 5,
    "interests": "nature, hiking",
    "accommodation_budget": "moderate",
    "dietary_preferences": "vegetarian",
    "food_budget": "medium"
  }
  ```

  **Response** (JSON):
  ```json
  {
    "finder_results": "Suggested stops and food options...",
    "itinerary": "| Day | Time | Activity / Place | Food & Dining | Accommodation & Travel Tips |\n|-----|------|------------------|---------------|-----------------------------|\n..."
  }
  ```

### Docker Deployment

Build and run the application using Docker:

```bash
docker build -t road-trip-planner .
docker run -p 8080:8080 -e GEMINI_API_KEY=your_api_key road-trip-planner
```

## Project Structure

- `main.py`: Streamlit application for the web interface.
- `app.py`: FastAPI application for the REST API.
- `graph.py`: Defines the LangGraph pipeline for trip planning.
- `nodes.py`: Contains the node functions for intent mapping, finder, and itinerary generation.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Docker configuration for containerization.
- `cloudbuild.yaml`: Google Cloud Build configuration.

## How It Works

The application uses a graph-based pipeline implemented with LangGraph:

1. **Intent Mapper Node**: Validates input fields and sets the trip planning intent.
2. **Finder Node**: Performs real-time search using DuckDuckGo to find scenic stops, attractions, and food options along the route, then uses Google Gemini to generate suggestions based on user preferences.
3. **Itinerary Node**: Creates a detailed day-by-day itinerary in Markdown table format, incorporating activities, food recommendations, and accommodation tips.

The pipeline processes user input through these nodes sequentially to produce a comprehensive trip plan.

## Dependencies

- `streamlit`: Web app framework
- `fastapi`: API framework
- `uvicorn`: ASGI server for FastAPI
- `pydantic`: Data validation
- `langchain-google-genai`: Google Gemini integration
- `langgraph`: Graph-based workflow management
- `duckduckgo-search`: Real-time web search
- `dotenv`: Environment variable management

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
