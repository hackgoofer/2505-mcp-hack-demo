import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient
from pydantic import BaseModel

app = FastAPI()
load_dotenv()

config = {
    "mcpServers": {
        "github": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "-e",
                "GITHUB_TOOLSETS",
                "ghcr.io/github/github-mcp-server",
            ],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv(
                    "GITHUB_PERSONAL_ACCESS_TOKEN"
                ),
                "GITHUB_TOOLSETS": "repos,issues,pull_requests,code_security,experiments",
            },
        }
    }
}

client = MCPClient.from_dict(config)
llm = ChatAnthropic(model="claude-3-7-sonnet-20250219")
agent = MCPAgent(llm=llm, client=client, max_steps=30)


class QueryRequest(BaseModel):
    query: str


@app.get("/test")
def test_endpoint():
    return {"message": "Server is working"}


@app.post("/run")
def run_agent(request: QueryRequest):
    print(f"Running agent with query: {request.query}")
    try:
        # Use asyncio.run to run the async function from a synchronous context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(agent.run(request.query))
        loop.close()
        return {"result": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
