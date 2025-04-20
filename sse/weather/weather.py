from typing import Any, Dict, List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import httpx
import json
import asyncio
from datetime import datetime

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Tool definitions
TOOLS = [
    {
        "name": "get_alerts",
        "description": "Get weather alerts for a US state",
        "parameters": {
            "state": {
                "type": "string",
                "description": "Two-letter US state code (e.g. CA, NY)"
            }
        }
    },
    {
        "name": "get_forecast",
        "description": "Get weather forecast for a location",
        "parameters": {
            "latitude": {
                "type": "number",
                "description": "Latitude of the location"
            },
            "longitude": {
                "type": "number",
                "description": "Longitude of the location"
            }
        }
    }
]

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location."""
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

def make_jsonrpc_response(id: int, result: Any) -> Dict:
    """Create a JSON-RPC response."""
    return {
        "jsonrpc": "2.0",
        "id": id,
        "result": result
    }

@app.post("/")
async def handle_jsonrpc(request: Request):
    """JSON-RPC 요청 처리"""
    data = await request.json()
    method = data.get("method")
    params = data.get("params", {})
    id = data.get("id")

    if method == "resources/list":
        return make_jsonrpc_response(id, {"resources": []})
    elif method == "prompts/list":
        return make_jsonrpc_response(id, {"prompts": []})
    elif method == "tools/list":
        return make_jsonrpc_response(id, {"tools": TOOLS})
    
    return make_jsonrpc_response(id, {"error": "Method not found"})

@app.get("/sse")
async def sse_endpoint(request: Request):
    """MCP SSE 엔드포인트"""
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            # 서버가 실행 중임을 알리는 하트비트 메시지
            yield {
                "event": "message",
                "data": json.dumps({
                    "type": "heartbeat",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            }

            await asyncio.sleep(30)  # 30초마다 하트비트

    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    import uvicorn
    print("Weather MCP SSE 서버를 시작합니다...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
