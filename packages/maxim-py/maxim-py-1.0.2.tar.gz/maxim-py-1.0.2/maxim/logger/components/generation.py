import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

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
        BaseContainer._commit_(writer,
                               Entity.GENERATION, id, "result", {"result": result})
        BaseContainer._end_(writer, Entity.GENERATION, id, {
            "endTimestamp": datetime.now(),
        })

    @staticmethod
    def end_(writer: LogWriter, id: str, data: Optional[Dict[str, Any]] = None):
        if data is None:
            data = {}
        BaseContainer._end_(writer, Entity.GENERATION, id, {
            "endTimestamp": datetime.now(),
            **data,
        })

    @staticmethod
    def add_tag_(writer: LogWriter, id: str, key: str, value: str):
        BaseContainer._add_tag_(writer, Entity.GENERATION, id, key, value)

    def result(self, result: Any):
        self._commit("result", {"result": result})
        self.end()

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
