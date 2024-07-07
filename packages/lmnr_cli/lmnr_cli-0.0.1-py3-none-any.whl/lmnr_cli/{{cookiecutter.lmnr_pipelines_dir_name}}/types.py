from dataclasses import dataclass
from typing import Union
import uuid
import datetime


@dataclass
class ChatMessage:
    role: str
    content: str

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        return cls(
            role=data["role"],
            content=data["content"],
        )


ChatMessageList = list[ChatMessage]


NodeInput = Union[str, ChatMessageList]  # TODO: Add conditioned value


@dataclass
class Message:
    id: uuid.UUID
    # output value of producing node in form of NodeInput
    # for the following consumer
    value: NodeInput
    # all input messages to this node; accumulates previous messages too
    # input_messages: list["Message"]
    start_time: datetime.datetime
    end_time: datetime.datetime
    # node_id: uuid.UUID
    # node_name: str
    # node_type: str
    # all node per-run metadata that needs to be logged at the end of execution
    # meta_log: MetaLog | None

    @classmethod
    def empty(cls) -> "Message":
        return cls(
            id=uuid.uuid4(),
            value="",
            # input_messages=[],
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            # node_id=uuid.uuid4(),
            # node_name="",
            # node_type="",
        )
