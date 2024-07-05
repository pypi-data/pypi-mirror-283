from typing import Any, Literal

from pydantic import BaseModel, Field


class NativeToolParam(BaseModel):
    type: Literal["string", "integer", "number", "boolean", "null"]


class ArrayToolParam(BaseModel):
    type: Literal["array"] = "array"
    items: list[Any]


class ObjectToolParam(BaseModel):
    type: Literal["object"] = "object"
    properties: dict[str, Any] = Field(
        default_factory=dict
    )
    required: list[str] = Field(default_factory=list)


class FunctionJsonSchema(BaseModel):
    name: str
    description: str = ""
    parameters: ObjectToolParam = Field(default_factory=ObjectToolParam)


ArrayToolParam.update_forward_refs()
ObjectToolParam.update_forward_refs()
