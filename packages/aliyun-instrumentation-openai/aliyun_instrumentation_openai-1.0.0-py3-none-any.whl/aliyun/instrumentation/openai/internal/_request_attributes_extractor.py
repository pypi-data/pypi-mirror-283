import json
import logging
from enum import Enum
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Iterator,
    List,
    Mapping,
    Tuple,
    Type,
)

from aliyun.instrumentation.openai.internal._utils import _get_openai_version
from aliyun.semconv.trace import MessageAttributes, SpanAttributes, ToolCallAttributes
from opentelemetry.util.types import AttributeValue

if TYPE_CHECKING:
    from openai.types import Completion, CreateEmbeddingResponse
    from openai.types.chat import ChatCompletion

__all__ = ("_RequestAttributesExtractor",)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class _RequestAttributesExtractor:
    __slots__ = (
        "_openai",
        "_chat_completion_type",
        "_completion_type",
        "_create_embedding_response_type",
    )

    def __init__(self, openai: ModuleType) -> None:
        self._openai = openai
        self._chat_completion_type: Type["ChatCompletion"] = openai.types.chat.ChatCompletion
        self._completion_type: Type["Completion"] = openai.types.Completion
        self._create_embedding_response_type: Type["CreateEmbeddingResponse"] = (
            openai.types.CreateEmbeddingResponse
        )

    def get_attributes_from_request(
            self,
            cast_to: type,
            request_parameters: Mapping[str, Any],
    ) -> Iterator[Tuple[str, AttributeValue]]:
        if not isinstance(request_parameters, Mapping):
            return
        if cast_to is self._chat_completion_type:
            yield from _get_attributes_from_chat_completion_create_param(request_parameters)
        elif cast_to is self._create_embedding_response_type:
            yield from _get_attributes_from_embedding_create_param(request_parameters)
        elif cast_to is self._completion_type:
            yield from _get_attributes_from_completion_create_param(request_parameters)
        else:
            try:
                if "temperature" in request_parameters:
                    yield SpanAttributes.GEN_AI_REQUEST_TEMPERATURE, request_parameters["temperature"]
            except Exception:
                logger.exception("Failed to serialize request options")


def _serialize_json(obj: Any) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


def _get_attributes_from_chat_completion_create_param(
        params: Mapping[str, Any],
) -> Iterator[Tuple[str, AttributeValue]]:
    # openai.types.chat.completion_create_params.CompletionCreateParamsBase
    # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/chat/completion_create_params.py#L28  # noqa: E501
    if not isinstance(params, Mapping):
        return
    invocation_params = dict(params)
    invocation_params.pop("messages", None)
    invocation_params.pop("functions", None)
    invocation_params.pop("tools", None)
    if (tools := params.get("tools")) and isinstance(tools, Iterable):
        for index, tool in enumerate(list(tools)):
            if "type" in dict(tool) and tool["type"] == "function":
                if "function" in tool:
                    tool_func = dict(tool["function"])
                    if "name" in tool_func:
                        yield f"{SpanAttributes.GEN_AI_REQUEST_TOOL_CALLS}.{index}.{SpanAttributes.TOOL_NAME}", tool_func["name"]
                    if "parameters" in tool_func:
                        yield f"{SpanAttributes.GEN_AI_REQUEST_TOOL_CALLS}.{index}.{SpanAttributes.TOOL_PARAMETERS}", json.dumps(
                            tool_func["parameters"], default=_serialize_json, ensure_ascii=False)
                    if "description" in tool_func:
                        yield f"{SpanAttributes.GEN_AI_REQUEST_TOOL_CALLS}.{index}.{SpanAttributes.TOOL_DESCRIPTION}", json.dumps(
                            tool_func["description"], default=_serialize_json, ensure_ascii=False)
    if "temperature" in invocation_params:
        yield SpanAttributes.GEN_AI_REQUEST_TEMPERATURE, invocation_params["temperature"]
    if "model" in invocation_params:
        yield SpanAttributes.GEN_AI_MODEL_NAME, invocation_params["model"]
        yield SpanAttributes.GEN_AI_REQUEST_MODEL_NAME, invocation_params["model"]
    if (input_messages := params.get("messages")) and isinstance(input_messages, Iterable):
        # Use reversed() to get the last message first. This is because OTEL has a default limit of
        # 128 attributes per span, and flattening increases the number of attributes very quickly.
        for index, input_message in reversed(list(enumerate(input_messages))):
            for key, value in _get_attributes_from_message_param(input_message):
                yield f"{SpanAttributes.GEN_AI_PROMPT}.{index}.{key}", value


def _get_attributes_from_message_param(
        message: Mapping[str, Any],
) -> Iterator[Tuple[str, AttributeValue]]:
    # openai.types.chat.ChatCompletionMessageParam
    # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/chat/chat_completion_message_param.py#L15  # noqa: E501
    if not hasattr(message, "get"):
        return
    if role := message.get("role"):
        yield (
            MessageAttributes.MESSAGE_ROLE,
            role.value if isinstance(role, Enum) else role,
        )
    if content := message.get("content"):
        if isinstance(content, str):
            yield MessageAttributes.MESSAGE_CONTENT, content
        elif isinstance(content, List):
            # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/chat/chat_completion_user_message_param.py#L14  # noqa: E501
            try:
                json_string = json.dumps(content)
            except Exception:
                logger.exception("Failed to serialize message content")
            else:
                yield MessageAttributes.MESSAGE_CONTENT, json_string
    if name := message.get("name"):
        yield MessageAttributes.MESSAGE_NAME, name
    if (function_call := message.get("function_call")) and hasattr(function_call, "get"):
        # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/chat/chat_completion_assistant_message_param.py#L13  # noqa: E501
        if function_name := function_call.get("name"):
            yield MessageAttributes.MESSAGE_FUNCTION_CALL_NAME, function_name
        if function_arguments := function_call.get("arguments"):
            yield (
                MessageAttributes.MESSAGE_FUNCTION_CALL_ARGUMENTS_JSON,
                function_arguments,
            )
    if (
            _get_openai_version() >= (1, 1, 0)
            and (tool_calls := message.get("tool_calls"),)
            and isinstance(tool_calls, Iterable)
    ):
        for index, tool_call in enumerate(tool_calls):
            # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/chat/chat_completion_message_tool_call_param.py#L23  # noqa: E501
            if not hasattr(tool_call, "get"):
                continue
            if (function := tool_call.get("function")) and hasattr(function, "get"):
                # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/chat/chat_completion_message_tool_call_param.py#L10  # noqa: E501
                if name := function.get("name"):
                    yield (
                        f"{MessageAttributes.MESSAGE_TOOL_CALLS}.{index}."
                        f"{ToolCallAttributes.TOOL_CALL_FUNCTION_NAME}",
                        name,
                    )
                if arguments := function.get("arguments"):
                    yield (
                        f"{MessageAttributes.MESSAGE_TOOL_CALLS}.{index}."
                        f"{ToolCallAttributes.TOOL_CALL_FUNCTION_ARGUMENTS_JSON}",
                        arguments,
                    )


def _get_attributes_from_completion_create_param(
        params: Mapping[str, Any],
) -> Iterator[Tuple[str, AttributeValue]]:
    # openai.types.completion_create_params.CompletionCreateParamsBase
    # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/completion_create_params.py#L11  # noqa: E501
    if not isinstance(params, Mapping):
        return
    invocation_params = dict(params)
    invocation_params.pop("prompt", None)
    if "temperature" in invocation_params:
        yield SpanAttributes.GEN_AI_REQUEST_TEMPERATURE, invocation_params["temperature"]
    if "model" in invocation_params:
        yield SpanAttributes.GEN_AI_MODEL_NAME, invocation_params["model"]
        yield SpanAttributes.GEN_AI_REQUEST_MODEL_NAME, invocation_params["model"]


def _get_attributes_from_embedding_create_param(
        params: Mapping[str, Any],
) -> Iterator[Tuple[str, AttributeValue]]:
    # openai.types.EmbeddingCreateParams
    # See https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/types/embedding_create_params.py#L11  # noqa: E501
    if not isinstance(params, Mapping):
        return
    invocation_params = dict(params)
    invocation_params.pop("input", None)
    if "temperature" in invocation_params:
        yield SpanAttributes.GEN_AI_REQUEST_TEMPERATURE, invocation_params["temperature"]
