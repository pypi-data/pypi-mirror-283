from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, cast

from langchain_core.load.serializable import Serializable
from langchain_core.pydantic_v1 import Extra, Field
from langchain_core.utils import get_bolded_text
from langchain_core.utils._merge import merge_dicts, merge_lists
from langchain_core.utils.interactive_env import is_interactive_env

from langchain_core.prompts.chat import ChatPromptTemplate

from langchain_core.messages.ai import AIMessage, AIMessageChunk
from langchain_core.messages.base import BaseMessage, BaseMessageChunk
from langchain_core.messages.chat import ChatMessage, ChatMessageChunk
from langchain_core.messages.function import FunctionMessage, FunctionMessageChunk
from langchain_core.messages.human import HumanMessage, HumanMessageChunk
from langchain_core.messages.system import SystemMessage, SystemMessageChunk
from langchain_core.messages.tool import ToolMessage, ToolMessageChunk

AnyMessage = Union[
    AIMessage, HumanMessage, ChatMessage, SystemMessage, FunctionMessage, ToolMessage
]

def get_buffer_string(
    messages: Sequence[BaseMessage], human_prefix: str = "Human", ai_prefix: str = "AI"
) -> str:
    """Convert a sequence of Messages to strings and concatenate them into one string.

    Args:
        messages: Messages to be converted to strings.
        human_prefix: The prefix to prepend to contents of HumanMessages.
        ai_prefix: THe prefix to prepend to contents of AIMessages.

    Returns:
        A single string concatenation of all input messages.

    Example:
        .. code-block:: python

            from langchain_core import AIMessage, HumanMessage

            messages = [
                HumanMessage(content="Hi, how are you?"),
                AIMessage(content="Good, how are you?"),
            ]
            get_buffer_string(messages)
            # -> "Human: Hi, how are you?\nAI: Good, how are you?"
    """
    string_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            role = human_prefix
        elif isinstance(m, AIMessage):
            role = ai_prefix
        elif isinstance(m, SystemMessage):
            role = "System"
        elif isinstance(m, FunctionMessage):
            role = "Function"
        elif isinstance(m, ToolMessage):
            role = "Tool"
        elif isinstance(m, ChatMessage):
            role = m.role
        else:
            raise ValueError(f"Got unsupported message type: {m}")
        message = f"{role}: {m.content}"
        if isinstance(m, AIMessage) and "function_call" in m.additional_kwargs:
            message += f"{m.additional_kwargs['function_call']}"
        string_messages.append(message)

    return "\n".join(string_messages)


class BaseMessage(Serializable):
    """Base abstract message class.

    Messages are the inputs and outputs of ChatModels.
    """

    content: Union[str, List[Union[str, Dict]]]
    """The string contents of the message."""

    additional_kwargs: dict = Field(default_factory=dict)
    """Reserved for additional payload data associated with the message.
    
    For example, for a message from an AI, this could include tool calls as
    encoded by the model provider.
    """

    response_metadata: dict = Field(default_factory=dict)
    """Response metadata. For example: response headers, logprobs, token counts."""

    type: str
    """The type of the message. Must be a string that is unique to the message type.
    
    The purpose of this field is to allow for easy identification of the message type
    when deserializing messages.
    """

    name: Optional[str] = None
    """An optional name for the message. 
    
    This can be used to provide a human-readable name for the message.
    
    Usage of this field is optional, and whether it's used or not is up to the
    model implementation.
    """

    id: Optional[str] = None
    """An optional unique identifier for the message. This should ideally be
    provided by the provider/model which created the message."""

    from_user: Optional[str] = None
    """An optional identifier for the user who sent the message."""

    from_id: Optional[str] = None
    """An optional unique identifier for the sender of the message."""

    context: Optional[Dict[str, Any]] = None
    """An optional context for the message. This can be a JSON object."""

    class Config:
        extra = Extra.allow

    def __init__(
        self, content: Union[str, List[Union[str, Dict]]], **kwargs: Any
    ) -> None:
        """Pass in content as positional arg."""
        super().__init__(content=content, **kwargs)

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        return True

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "schema", "messages"]

    def __add__(self, other: Any) -> ChatPromptTemplate:
        """Concatenate this message with another message."""
        from langchain_core.prompts.chat import ChatPromptTemplate

        prompt = ChatPromptTemplate(messages=[self])  # type: ignore[call-arg]
        return prompt + other

    def pretty_repr(self, html: bool = False) -> str:
        title = get_msg_title_repr(self.type.title() + " Message", bold=html)
        # TODO: handle non-string content.
        if self.name is not None:
            title += f"\nName: {self.name}"
        if self.from_user is not None:
            title += f"\nFrom User: {self.from_user}"
        if self.from_id is not None:
            title += f"\nFrom ID: {self.from_id}"
        if self.context is not None:
            title += f"\nContext: {self.context}"
        return f"{title}\n\n{self.content}"

    def pretty_print(self) -> None:
        print(self.pretty_repr(html=is_interactive_env()))  # noqa: T201


from typing import Sequence, List, Dict, Any

def messages_from_dict(messages: Sequence[Dict[str, Any]]) -> List[BaseMessage]:
    """Convert a sequence of messages from dicts to Message objects.

    Args:
        messages: Sequence of messages (as dicts) to convert.

    Returns:
        List of messages (BaseMessages).
    """
    return [_message_from_dict(m) for m in messages]

def _message_from_dict(message_dict: Dict[str, Any]) -> BaseMessage:
    """Convert a single message from a dict to a BaseMessage object.

    Args:
        message_dict: Message as a dict.

    Returns:
        BaseMessage object.
    """
    message_type = message_dict.pop("type")
    content = message_dict.pop("content")
    additional_kwargs = message_dict.pop("additional_kwargs", {})
    response_metadata = message_dict.pop("response_metadata", {})
    name = message_dict.pop("name", None)
    id = message_dict.pop("id", None)
    from_user = message_dict.pop("from_user", None)
    from_id = message_dict.pop("from_id", None)
    context = message_dict.pop("context", None)
    role = message_dict.pop("role", None)

    # Any remaining keys are considered extra and should be added to additional_kwargs
    additional_kwargs.update(message_dict)

    return BaseMessage(
        content=content,
        type=message_type,
        additional_kwargs=additional_kwargs,
        response_metadata=response_metadata,
        name=name,
        id=id,
        from_user=from_user,
        from_id=from_id,
        context=context, 
        role=role
    )

def message_to_dict(message: BaseMessage) -> Dict[str, Any]:
    """Convert a Message to a dictionary.

    Args:
        message: Message to convert.

    Returns:
        Message as a dict.
    """
    message_dict = message.dict()
    message_dict["role"] = getattr(message, "role", "ai")
    message_dict["type"] = getattr(message, "type", "ai")
    message_dict["from_user"] = getattr(message, "from_user", None)
    message_dict["from_id"] = getattr(message, "from_id", None)
    message_dict["context"] = getattr(message, "context", None)
    return message_dict