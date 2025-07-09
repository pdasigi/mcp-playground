import asyncio
import argparse

from agents import Agent, Runner, trace
from agents.mcp import MCPServer, MCPServerStdio
from agents.extensions.models.litellm_model import LitellmModel


async def run(mcp_server: MCPServer, model_type: str, vllm_model_name: str, port: int):
    if model_type == "openai":
        model = None
    else:
        model = LitellmModel(
            model=f"hosted_vllm/{vllm_model_name}",
            base_url=f"http://localhost:{port}/v1",
            api_key="EMPTY",
        )
    agent = Agent(
        name="Assistant",
        instructions="Answer questions about the papers on Semantic Scholar.",
        model=model,
        mcp_servers=[mcp_server],
    )

    #message = "Retrieve the list of the papers co-authored by Pradeep Dasigi and summarize the research topics based on the titles."
    message = "Give me a list of the papers co-authored by Pradeep Dasigi."
    print("\n" + "-" * 40)
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main(model_type: str, vllm_model_name: str, port: int):

    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        params={
            "command": "npx",
            "args": [
                "mcp-remote",
                "https://api.semanticscholar.org/mcp",
            ]
        },
    ) as server:
        with trace(workflow_name="MCP S2 Example"):
            await run(server, model_type=model_type, vllm_model_name=vllm_model_name, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_type",
        type=str,
        default="openai",
        choices=["openai", "vllm"],
    )
    parser.add_argument(
        "--vllm_model_name",
        type=str,
        default="allenai/general-tool-use-dev",
        help="Model name to use for the agent.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="VLLM server port to connect to.",
    )
    args = parser.parse_args()

    asyncio.run(main(model_type=args.model_type, vllm_model_name=args.vllm_model_name, port=args.port))