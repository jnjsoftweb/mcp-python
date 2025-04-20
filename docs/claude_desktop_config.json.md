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
		"weather": {
			"command": "sh",
			"args": [
				"-c",
				"npx -y supergateway --sse http://localhost:8001/sse"
			]
		}
	}
}

## Success !!!

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