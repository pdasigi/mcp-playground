from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        # {
        #     "type": "mcp",
        #     "server_label": "deepwiki",
        #     "server_url": "https://mcp.deepwiki.com/mcp",
        #     "require_approval": "never",
        # },
        {
            "type": "mcp",
            "server_label": "semanticscholar",
            "server_url": "https://api.semanticscholar.org/mcp",
            "require_approval": "never",
        }
    ],
    input="List the papers written by Pradeep Dasigi.",
)

print(resp.output_text)