"""This module contains the setup_call function for Cohere tools."""

import inspect
from typing import Any, Awaitable, Callable

from cohere import AsyncClient, Client
from cohere.types import ChatMessage, NonStreamedChatResponse

from ...base import BaseMessageParam, BaseTool, _utils
from ..call_params import CohereCallParams
from ..dynamic_config import CohereDynamicConfig
from ..tool import CohereTool


def setup_call(
    *,
    model: str,
    client: Client | AsyncClient | None,
    fn: Callable[..., CohereDynamicConfig | Awaitable[CohereDynamicConfig]],
    fn_args: dict[str, Any],
    dynamic_config: CohereDynamicConfig,
    tools: list[type[BaseTool] | Callable] | None,
    json_mode: bool,
    call_params: CohereCallParams,
    extract: bool,
) -> tuple[
    Callable[..., NonStreamedChatResponse]
    | Callable[..., Awaitable[NonStreamedChatResponse]],
    str,
    list[BaseMessageParam],
    list[type[CohereTool]] | None,
    dict[str, Any],
]:
    prompt_template, messages, tool_types, call_kwargs = _utils.setup_call(
        fn, fn_args, dynamic_config, tools, CohereTool, call_params
    )
    if client is None:
        client = AsyncClient() if inspect.iscoroutinefunction(fn) else Client()

    preamble = ""
    if "preamble" in call_kwargs and call_kwargs["preamble"] is not None:
        preamble += call_kwargs.pop("preamble")
    if messages[0]["role"] == "SYSTEM":
        preamble += messages.pop(0)["content"]
    if preamble:
        call_kwargs["preamble"] = preamble
    if len(messages) > 1:
        call_kwargs["chat_history"] = [
            ChatMessage(role=message["role"].upper(), message=message["content"])  # type: ignore
            for message in messages[:-1]
        ]
    call_kwargs |= {
        "model": model,
        "message": messages[-1]["content"],
    }
    if json_mode:
        messages[-1]["content"] += _utils.json_mode_content(
            tool_types[0] if tool_types else None
        )
        call_kwargs.pop("tools", None)
    elif extract:
        assert tool_types, "At least one tool must be provided for extraction."

    def create_or_stream(stream: bool, **kwargs: Any):
        if stream:
            return client.chat_stream(**kwargs)
        return client.chat(**kwargs)

    return create_or_stream, prompt_template, messages, tool_types, call_kwargs  # type: ignore
