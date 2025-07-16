from typing import Sequence

from vllm.entrypoints.openai.tool_parsers.pythonic_tool_parser import PythonicToolParser
from vllm.entrypoints.openai.tool_parsers.abstract_tool_parser import ToolParserManager
from vllm.entrypoints.openai.protocol import (ChatCompletionRequest, DeltaMessage,
                                              ExtractedToolCallInformation)


@ToolParserManager.register_module("toolu_pythonic")
class TooluPythonicToolParser(PythonicToolParser):
    """A custom tool parser for Toolu that extends the PythonicToolParser."""
 
    def extract_tool_calls(
            self, model_output: str,
            request: ChatCompletionRequest
    ) -> ExtractedToolCallInformation:
        model_output = model_output.replace("<function_calls>", "").replace("</function_calls>", "")
        model_output = model_output.replace("\n", ", ")
        model_output = f"[{model_output}]"
        extracted_tool_call_info = super().extract_tool_calls(model_output, request)
        return extracted_tool_call_info

    def extract_tool_calls_streaming(self,
                                     previous_text: str,
                                     current_text: str,
                                     delta_text: str,
                                     previous_token_ids: Sequence[int],
                                     current_token_ids: Sequence[int],
                                     delta_token_ids: Sequence[int],
                                     request: ChatCompletionRequest
    ) -> DeltaMessage | None:
        # TODO: Figure out how the streaming extractor works.
        raise NotImplementedError(
            "Streaming tool call extraction is not supported in TooluPythonicToolParser."
        )