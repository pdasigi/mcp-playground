# mcp-playground
This code shows examples of how open-weight models trained for function calling can be used with OpenAI Agents SDK to communicate with MCP servers.

## Run a vLLM server
The first step is to run a vLLM server with the appropriate tool call parser and optionally the right chat template. See [vLLM's function calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for more information.

The tool call parser transforms the output from the model into a standardized format that frameworks like OpenAI Agents SDK understand. vLLM has some in-built tool call parsers. You can also provide one as a plugin instead. The chat template should identify tools provided to the agent and add it to the model's context appropriately, e.g., within the system prompt. If the model's default chat template does not do this already, you can provide one as a local file.

Run one of the following depending on which model you want to serve.

```
./run_qwen3_vllm_server.sh
```
or
```
./run_toolu_vllm_server.sh
```

## Running the agent with an MCP server
Once the vLLM server is up and running, run
```
python agents_with_s2_mcpy.py
```
with the appropriate arguments. You can either use the vLLM server, or a default OpenAI model with the same MCP server. This example uses the Seamntic Scholar MCP server.

If you set your `OPENAI_API_KEY`, you can trace your agent's execution [here](https://platform.openai.com/traces).