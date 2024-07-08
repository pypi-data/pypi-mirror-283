import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from ..writer import LogWriter
from .base import BaseContainer
from .types import Entity


@dataclass
class GenerationConfig:
    id: str
    provider: str
    model: str
    messages: List[Any] = field(default_factory=list)
    model_parameters: Dict[str, Any] = field(default_factory=dict)
    span_id: Optional[str] = None
    name: Optional[str] = None
    maxim_prompt_id: Optional[str] = None
    tags: Optional[Dict[str, str]] = None


@dataclass
class Choice:
    index: int
    text: str
    logprobs: Optional[object] = None
    finish_reason: Optional[str] = None


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class GenerationError:
    message: str
    code: Optional[str] = None
    type: Optional[str] = None


@dataclass
class TextCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    error: Optional[GenerationError] = None


# Validators
def validate_type(value, expected_type, field_name):
    if not isinstance(value, expected_type):
        raise ValueError(
            f"{field_name} must be of type {expected_type.__name__}")


def validate_choice(choice_data):
    validate_type(choice_data.get('index'), int, 'index')
    validate_type(choice_data.get('text'), str, 'text')
    validate_type(choice_data.get('finish_reason'), str, 'finish_reason')
    return Choice(**choice_data)


def validate_usage(usage_data):
    validate_type(usage_data.get('prompt_tokens'), int, 'prompt_tokens')
    validate_type(usage_data.get('completion_tokens'),
                  int, 'completion_tokens')
    validate_type(usage_data.get('total_tokens'), int, 'total_tokens')
    return Usage(**usage_data)


def validate_text_completion(data: dict) -> TextCompletion:
    validate_type(data.get('id'), str, 'id')
    validate_type(data.get('object'), str, 'object')
    validate_type(data.get('created'), int, 'created')
    validate_type(data.get('model'), str, 'model')

    choices_data = data.get('choices')
    validate_type(choices_data, list, 'choices')
    if not choices_data:
        raise ValueError("choices must not be empty")
    choices = [validate_choice(choice) for choice in choices_data]

    usage = validate_usage(data.get('usage', {}))

    return TextCompletion(
        id=data['id'],
        object=data['object'],
        created=data['created'],
        model=data['model'],
        choices=choices,
        usage=usage,
        error=GenerationError(data.get('error', None))
    )


# Main class
class Generation(BaseContainer):
    def __init__(self, config: GenerationConfig, writer: LogWriter):
        super().__init__(Entity.GENERATION, config.__dict__, writer)
        self.model = config.model
        self.maxim_prompt_id = config.maxim_prompt_id
        self.messages = []
        self.provider = config.provider
        self.messages.extend(config.messages)
        self.model_parameters = config.model_parameters

    @staticmethod
    def set_model_(writer: LogWriter, id: str, model: str):
        BaseContainer._commit_(writer, Entity.GENERATION,
                               id, "update", {"model": model})

    def set_model(self, model: str):
        self.model = model
        self._commit("update", {"model": model})

    @staticmethod
    def add_message_(writer: LogWriter, id: str, message: Any):
        BaseContainer._commit_(writer, Entity.GENERATION, id, "update", {
            "messages": [message]})

    def add_message(self, message: Any):
        self.messages.append(message)
        self._commit("update", {"messages": [message]})

    @staticmethod
    def set_model_parameters_(writer: LogWriter, id: str, model_parameters: Dict[str, Any]):
        BaseContainer._commit_(writer, Entity.GENERATION, id, "update", {
            "model_parameters": model_parameters})

    def set_model_parameters(self, model_parameters: Dict[str, Any]):
        self.model_parameters = model_parameters
        self._commit("update", {"model_parameters": model_parameters})

    @staticmethod
    def result_(writer: LogWriter, id: str, result: Any):
        try:
            validate_text_completion(result)
            BaseContainer._commit_(writer,
                                   Entity.GENERATION, id, "result", {"result": result})
            BaseContainer._end_(writer, Entity.GENERATION, id, {
                "endTimestamp": datetime.now(timezone.utc),
            })
        except ValueError as e:
            raise ValueError(
                f"Invalid result. We expect OpenAI response format: {e}")

    @staticmethod
    def end_(writer: LogWriter, id: str, data: Optional[Dict[str, Any]] = None):
        if data is None:
            data = {}
        BaseContainer._end_(writer, Entity.GENERATION, id, {
            "endTimestamp": datetime.now(timezone.utc),
            **data,
        })

    @staticmethod
    def add_tag_(writer: LogWriter, id: str, key: str, value: str):
        BaseContainer._add_tag_(writer, Entity.GENERATION, id, key, value)

    def result(self, result: Any):
        try:
            validate_text_completion(result)
            self._commit("result", {"result": result})
            self.end()
        except ValueError as e:
            raise ValueError(
                f"Invalid result. We expect OpenAI response format: {e}")

    def error(self, error: GenerationError):
        if not error.code:
            error.code = ""
        if not error.type:
            error.type = ""
        self._commit("result", {"result": {"error": {
            "message": error.message,
            "code": error.code,
            "type": error.type,
        }, "id": str(uuid4())}})
        self.end()

    @staticmethod
    def error_(writer: LogWriter, id: str, error: GenerationError):
        if not error.code:
            error.code = ""
        if not error.type:
            error.type = ""
        BaseContainer._commit_(writer, Entity.GENERATION,
                               id, "result", {"result": {"error": {
                                   "message": error.message,
                                   "code": error.code,
                                   "type": error.type,
                               }, "id": str(uuid4())}})
        BaseContainer._end_(writer, Entity.GENERATION, id, {
            "endTimestamp": datetime.now(timezone.utc),
        })

    def data(self) -> Dict[str, Any]:
        base_data = super().data()
        return {
            **base_data,
            "model": self.model,
            "provider": self.provider,
            "maximPromptId": self.maxim_prompt_id,
            "messages": self.messages,
            "modelParameters": self.model_parameters,
        }
