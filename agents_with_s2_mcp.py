import asyncio
import argparse
import logging

from agents import Agent, Runner, trace
from agents.mcp import MCPServer, MCPServerStdio
from agents.extensions.models.litellm_model import LitellmModel

logger = logging.getLogger(__name__)


async def run(mcp_server: MCPServer, model: str, port: int):
    if model == "openai":
        _model = None
        logger.info("Using OpenAI model with MCP server.")
    else:
        model_name = "Qwen/Qwen3-8B" if model == "qwen" else "allenai/general-tool-use-dev"
        logger.info(f"Using VLLM model: {model_name} on port {port}.")
        _model = LitellmModel(
            model=f"hosted_vllm/{model_name}",
            base_url=f"http://localhost:{port}/v1",
            api_key="EMPTY",
        )
    agent = Agent(
        name="Assistant",
        instructions="Answer questions about the papers on Semantic Scholar.",
        model=_model,
        mcp_servers=[mcp_server],
    )

    #message = "Retrieve the list of the papers co-authored by Pradeep Dasigi and summarize the research topics based on the titles."
    message = "Tell me about the paper 'Attention is All You Need'"
    print("\n" + "-" * 40)
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main(model: str, port: int):

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
        with trace(workflow_name=f"S2 MCP with {model}"):
            await run(server, model=model, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="toolu",
        choices=["qwen", "toolu", "openai"],
        help="Model name to use for the agent.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="VLLM server port to connect to.",
    )
    args = parser.parse_args()

    asyncio.run(main(model=args.model, port=args.port))