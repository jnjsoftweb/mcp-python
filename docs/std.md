```sh
cd /Users/moon/JnJ/Developments/Servers/mcp/python/std
uv init mcp-server-demo
cd init mcp-server-demo


uv init weather
cd weather
```

```sh
# Create a new directory for our project
uv init weather
cd weather

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx

# Create our server file
touch weather.py
```