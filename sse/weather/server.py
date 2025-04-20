"""
Weather MCP Server using FastMCP with SSE Transport
"""

import sys
import json
import httpx
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP(name="Weather MCP Server")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Helper function to make requests to the NWS API
async def make_nws_request(url: str) -> Optional[Dict[str, Any]]:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    print(f"Making request to: {url}", file=sys.stderr)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API request error: {e}", file=sys.stderr)
            return None

# Format alert data into readable text
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

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    print(f"Fetching alerts for state: {state}", file=sys.stderr)
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    
    if not data["features"]:
        return "No active alerts for this state."
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forecast for a location.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    print(f"Fetching forecast for location: {latitude}, {longitude}", file=sys.stderr)
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(url=points_url)
    
    if not points_data:
        return "Unable to fetch forecast data for this location."
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(url=forecast_url)
    
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


if __name__ == "__main__":
    print("Starting Weather MCP Server with SSE transport...", file=sys.stderr)
    
    # 모든 인터페이스에서 접속 허용
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8001
    
    # 서버 실행
    mcp.run(transport="sse")
