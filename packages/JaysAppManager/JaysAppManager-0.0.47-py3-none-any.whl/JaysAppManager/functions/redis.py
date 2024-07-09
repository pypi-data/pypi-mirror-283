import json
import logging
from typing import Optional, List, Dict
from datetime import datetime

from JaysAppManager.functions.basemessage import BaseMessage, messages_from_dict, message_to_dict
from JaysAppManager.functions.chat_history import BaseChatMessageHistory

logger = logging.getLogger(__name__)



class RedisChatMessageHistory(BaseChatMessageHistory):
    """Chat message history stored in a Redis database."""

    def __init__(
        self,
        session_id: str,
        host: str = "172.18.0.10",
        port: int = 6379,
        password: str = "your_strong_password",
        db: int = 0,
        key_prefix: str = "message_store:",
        ttl: Optional[int] = None,
    ):
        try:
            import redis
        except ImportError:
            raise ImportError(
                "Could not import redis-py python package. "
                "Please install it with `pip install redis`."
            )

        self.redis_client = redis.Redis(host=host, port=port, username="default", password=password, db=db, decode_responses=True)
        self.session_id = session_id
        self.key_prefix = key_prefix
        self.ttl = ttl

    @property
    def key(self) -> str:
        """Construct the record key to use"""
        return self.key_prefix + self.session_id

    @property
    def messages(self) -> List[Dict[str, BaseMessage]]:
        """Retrieve the messages from Redis"""
        _items = self.redis_client.lrange(self.key, 0, -1)
        items = [json.loads(m) for m in _items[::-1]]
        messages = []
        for item in items:
            message_dict = item['message']
            timestamp = item['timestamp']
            message = messages_from_dict([message_dict])[0]
            messages.append({'message': message, 'timestamp': timestamp})
        return messages

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in Redis"""


            
        timestamp = datetime.now().isoformat()
        message_with_timestamp = {
            'message': message_to_dict(message),
            'timestamp': timestamp,
            'type' : message.type,
            'role' : "role"
        }
        self.redis_client.lpush(self.key, json.dumps(message_with_timestamp))
        if self.ttl:
            self.redis_client.expire(self.key, self.ttl)

    def clear(self) -> None:
        """Clear session memory from Redis"""
        self.redis_client.delete(self.key)

    def add_context(self, context) -> None:


        stype = context.get('type', 'context')

        if stype == "videodata":
            m = BaseMessage(content=context.get('content', ''), 
                type=context.get('type', 'context'),
                additional_kwargs = context.get('additional_kwargs', {}),
                response_metadata = context.get('response_metadata', {}),
                name = context.get('name', None),
                from_user = context.get('from_user', None),
                from_id = context.get('user_id', None),
                context = context.get('context', {})
            )
            print(m.__dict__)
            self.add_message(m)
        elif stype == "commanddata":
            m = BaseMessage(content=context.get('content', ''), 
                type=context.get('type', 'context'),
                additional_kwargs = context.get('additional_kwargs', {}),
                response_metadata = context.get('response_metadata', {}),
                name = context.get('name', None),
                from_user = context.get('from_user', None),
                from_id = context.get('user_id', None),
                context = context.get('context', {})
            )
            print(m.__dict__)
            self.add_message(m)
        else:
            print(f"The 'if' condition failed because the 'type' in context is not 'videodata'. The actual type is: {stype}")


        