import datetime
from datetime import datetime
from typing import Any, Literal, NotRequired, Optional, TypedDict

from pydantic import BaseModel, Field

from melting_schemas.meta import Creator
from melting_schemas.utils import StreamTimings, Timings

from ..completion.chat import ChatMLMessage, ChatModelSettings, Templating
from ..json_schema import FunctionJsonSchema
from ..meta import Creator
from ..utils import TokenUsage


class TCallModelSettings(BaseModel):
    model: str
    max_iterations: int = 10  # Maximum back and fourth allowed
    max_tokens: int | None = None  # defaults to inf
    temperature: float | None = None  # ValueRange(0, 2)
    top_p: float | None = None  # ValueRange(0, 1)
    frequency_penalty: float | None = None  # ValueRange(-2, 2) defaults to 0
    presence_penalty: float | None = None  # ValueRange(-2, 2) defaults to 0
    logit_bias: dict[str, int] | None = None  # valmap(ValueRange(-100, 100))
    stop: list[str] | None = None  # MaxLen(4)
    tool_choice: Literal["auto", "required"] = "auto"  # defaults to auto


class ToolCallChunk(TypedDict):
    index: int
    id: str
    name: str
    arguments: str


class ChatChunk(TypedDict, total=False):
    delta: str


class ToolCall(TypedDict):
    index: NotRequired[int]
    id: str
    name: str
    arguments: str
    response: NotRequired[Any]


class ToolCallMLMessage(TypedDict):
    content: Optional[str]
    tool_calls: list[ToolCall]
    role: Literal["assistant"]


class ToolMLMessage(TypedDict):
    tool_call_id: NotRequired[str]
    content: str
    name: str
    role: Literal["tool"]


class ToolJsonSchema(BaseModel):
    type: Literal["function"] = "function"
    function: FunctionJsonSchema


class StaticParams(BaseModel):
    query: dict[str, Any] = Field(default_factory=dict)
    body: dict[str, Any] = Field(default_factory=dict)


class DynamicParams(BaseModel):
    path: list[str] = Field(default_factory=list)
    query: list[str] = Field(default_factory=list)
    body: list[str] = Field(default_factory=list)


class ToolArgMap(BaseModel):
    location: str
    name: str


class HttpToolCallee(BaseModel):
    type: Literal["http"] = "http"
    method: Literal["GET", "POST"]
    forward_headers: list[str] = Field(default_factory=list)
    headers: dict[str, str] = Field(default_factory=dict)
    url: str
    static: StaticParams = Field(default_factory=StaticParams)
    dynamic: DynamicParams = Field(default_factory=DynamicParams)


class NoopToolCallee(BaseModel):
    type: Literal["noop"] = "noop"


class ToolSpec(BaseModel):
    name: str
    callee: HttpToolCallee | NoopToolCallee
    json_schema: ToolJsonSchema


class StaticToolRequest(BaseModel):
    name: str
    arguments: Optional[dict[str, Any]] = None
    response: dict | list | str | None = None


class TCallRequest(BaseModel):
    messages: list[ChatMLMessage | ToolCallMLMessage | ToolMLMessage]
    settings: TCallModelSettings
    static_tools: list[StaticToolRequest] = Field(default_factory=list)
    tools: list[ToolSpec] | list[ToolJsonSchema] | list[str] = Field(
        default_factory=list
    )

    class Config:
        smart_unions = True
        examples = {
            "Raw JSON schema": {
                "value": {
                    "tools": [
                        {
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "description": "Get the current weather in a given city.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "location": {
                                            "type": "string",
                                            "description": "The city and state, e.g. San Francisco, CA",
                                        }
                                    },
                                    "required": ["location"],
                                },
                            },
                        }
                    ],
                    "messages": [
                        {
                            "content": "What is the weather like in Boston?",
                            "role": "user",
                        }
                    ],
                    "settings": {
                        "model": "gpt-4o",
                        "tool_choice": "auto",
                    },
                }
            },
            "Raw JSON schema + static plugin request": {
                "value": {
                    "tools": [
                        {
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "description": "Get the current weather in a given city.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "location": {
                                            "type": "string",
                                            "description": "The city and state, e.g. San Francisco, CA",
                                        }
                                    },
                                    "required": ["location"],
                                },
                            },
                        }
                    ],
                    "static_tools": [
                        {
                            "name": "get_weather",
                            "arguments": {"location": "Boston"},
                            "response": {"temperature": 70, "weather": "sunny"},
                        }
                    ],
                    "messages": [
                        {
                            "content": "What is the weather like? @get_weather:Boston",
                            "role": "user",
                        }
                    ],
                    "settings": {
                        "model": "gpt-4o",
                        "tool_choice": "auto",
                    },
                }
            },
            "Volatile plugin": {
                "value": {
                    "tools": [
                        {
                            "type": "http",
                            "name": "my_function",
                            "callee": {
                                "method": "GET",
                                "forward_headers": ["x-user-email"],
                                "headers": {"authorization": "my-special-api-token"},
                                "url": "https://datasources.allai.digital/{name}/search",
                                "static": {
                                    "query": {"limit": 2},
                                    "body": {"top_k": 10},
                                },
                                "dynamic": {
                                    "path": ["name"],
                                    "body": ["top_k", "search_query"],
                                },
                            },
                            "json_schema": {
                                "type": "function",
                                "function": {
                                    "name": "my_function",
                                    "description": "This is my function",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "my_param": {
                                                "type": "string",
                                                "description": "This is my parameter",
                                            }
                                        },
                                        "required": ["my_param"],
                                    },
                                },
                            },
                        }
                    ],
                    "messages": [
                        {
                            "content": "Hello",
                            "role": "user",
                        }
                    ],
                    "settings": {
                        "model": "gpt-4o",
                        "tool_choice": "auto",
                    },
                }
            },
            "Persisted plugin": {
                "value": {
                    "tools": ["example-tool-name"],
                    "messages": [
                        {
                            "content": "Hello",
                            "role": "user",
                        }
                    ],
                    "settings": {
                        "model": "gpt-4o",
                        "tool_choice": "auto",
                    },
                }
            },
            "Persisted plugin (after selection)": {
                "tools": ["get_weather"],
                "messages": [
                    {"content": "What is the weather like in Boston?", "role": "user"},
                    {
                        "content": None,
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "function": {
                                    "args": '{"location": "Boston, MA"}',
                                    "name": "get_weather",
                                },
                                "id": 0,
                                "type": "function",
                            }
                        ],
                    },
                ],
                "settings": {
                    "model": "openai/gpt-4o-2024-05-13",
                },
            },
        }


class TCallProcessedRequest(BaseModel):
    messages: list[ChatMLMessage | ToolCallMLMessage | ToolMLMessage]
    settings: TCallModelSettings
    static_tools: list[StaticToolRequest]
    tools: list[ToolSpec] | list[ToolJsonSchema]


class TCallCompletionCreationResponse(BaseModel):
    created_at: datetime
    created_by: Creator
    finish_reason: Literal["stop", "length", "function_call", "tool_calls"]
    id: str = Field(..., alias="_id")
    messages: list[ChatMLMessage | ToolCallMLMessage | ToolMLMessage]
    tool_calls: list[ToolCall]
    output: ChatMLMessage | ToolMLMessage | ToolCallMLMessage
    settings: ChatModelSettings
    templating: Optional[Templating]
    timings: Timings | StreamTimings
    usage: TokenUsage

    class Config:
        smart_unions = True
