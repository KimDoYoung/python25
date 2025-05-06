# MCP-SERVER

## 개요

1. mcp demo 연습 프로젝트
2. 유튜브 따라서 코딩 [stick note](https://www.youtube.com/watch?v=-8k9lGpGQ6g)


## 배포

1. claude에 등록
* claude_desktop_config.json
```json
{
 "mcpServers": {
    "TestNotes": {
        "command" : "c:\\Users\\USER\\.local\\bin\\uv",
        "args" : [
            "run",
            "--with",
            "mcp[cli]",
            "mcp",
            "run",
            "c:\\Users\\USER\\work\\python25\\ai_ocr\\mcp-server-demo\\server.py"
        ]
    }
 }
}
```
2. vscode
* mcp.json
```json
{
    "inputs": [
      {
        "type": "promptString",
        "id": "github_token",
        "description": "Enter your GitHub Personal Access Token"
      }
    ],
    "servers": {
        "fetch": {
            "command": "uvx",
            "args": ["mcp-server-fetch"]
        },
        "playwright": {
            "command": "npx",
            "args": [
                "@playwright/mcp@latest",
                "--headless"
            ]
        }
    }
}
```


