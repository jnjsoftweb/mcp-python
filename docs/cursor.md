클로드 config.json을 아래와 같이 설정하고, 


{
	"mcpServers": {
		"markdown": {
			"command": "npx",
			"args": [
				"-y",
				"mcp-obsidian",
				"/Users/moon/Library/CloudStorage/GoogleDrive-mooninone@gmail.com/내 드라이브/Obsidian/_Master"
			]
		},
		"greeting": {
			"command": "sh",
			"args": [
				"-c",
				"npx -y supergateway --sse http://localhost:8003/sse"
			]
		}
	}
}


		"weather": {
			"command": "sh",
			"args": [
				"-c",
				"npx -y supergateway --sse http://localhost:8001/sse"
			]
		}

---

`/Users/moon/JnJ/Developments/Servers/mcp/python/sse/weather/greeting.py` 를

실행하였더니, 로그가 아래와 같이 뜨면서, 클로드 툴 추가 및 기능이 성공적이었어요.

uv run greeting.py
warning: `VIRTUAL_ENV=/Users/moon/JnJ/Developments/Servers/mcp/python/std/weather/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
INFO:     Started server process [5452]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
INFO:     127.0.0.1:64138 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:64139 - "POST /messages/?session_id=68cabe1f6d3f41018ed65f2f6d5636b8 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:64139 - "POST /messages/?session_id=68cabe1f6d3f41018ed65f2f6d5636b8 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:64139 - "POST /messages/?session_id=68cabe1f6d3f41018ed65f2f6d5636b8 HTTP/1.1" 202 Accepted
[04/20/25 20:48:57] INFO     Processing request of type ListResourcesRequest                         server.py:534
INFO:     127.0.0.1:64140 - "POST /messages/?session_id=68cabe1f6d3f41018ed65f2f6d5636b8 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:64141 - "POST /messages/?session_id=68cabe1f6d3f41018ed65f2f6d5636b8 HTTP/1.1" 202 Accepted


===

테스트를 성공한 '/Users/moon/JnJ/Developments/Servers/mcp/python/sse/weather/greeting.py' 파일을 꼼꼼히 살펴보고 참고하여, `/Users/moon/JnJ/Developments/Servers/mcp/python/sse/weather/weather.py` 파일의 기능은 유지한 채 mcp sse 서버를 `/Users/moon/JnJ/Developments/Servers/mcp/python/sse/weather/server.py`에 구현해주세요. 