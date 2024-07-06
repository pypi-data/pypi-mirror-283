# itba_microservices_rabbitmq_connectors/rabbitmq_dtos.py

from pydantic import BaseModel


class MqPersistNewMessageDto(BaseModel):
    eventId: str
    chatId: str
    content: str
    author: str


class MqGetLLMResponseDto(BaseModel):
    eventId: str
    chatId: str
    content: str


class MqLLMResponseDto(BaseModel):
    eventId: str
    chatId: str
    response: str
