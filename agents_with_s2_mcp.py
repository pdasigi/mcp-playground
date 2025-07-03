import asyncio

from agents import Agent, Runner, trace
from agents.mcp import MCPServer, MCPServerStdio


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="Answer questions about the papers on Semantic Scholar.",
        mcp_servers=[mcp_server],
    )

    message = "Give me a list of the papers written by Pradeep Dasigi."
    print("\n" + "-" * 40)
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():

    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        params={"command": "npx", "args": ["mcp-remote", "https://api.semanticscholar.org/mcp"]},
    ) as server:
        with trace(workflow_name="MCP S2 Example"):
            await run(server)


if __name__ == "__main__":
    asyncio.run(main())