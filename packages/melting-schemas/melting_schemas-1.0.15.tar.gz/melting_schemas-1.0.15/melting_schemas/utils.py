from typing import Literal, Required, TypedDict


class Timings(TypedDict):
    total: float


class StreamTimings(TypedDict):
    avg: float
    first: float
    max: float
    min: float
    total: float


class TokenUsage(TypedDict, total=False):
    prompt_tokens: Required[int]
    total_tokens: Required[int]
    completion_tokens: int


class UsageInfo(TypedDict):
    finish_reason: Literal[
        "stop", "length", "tool_calls", "content_filter", "function_call"
    ]
    token_usage: TokenUsage
    timings: StreamTimings
