from typing import Any, Dict, Optional, List, Tuple, Set
import threading
from uuid import uuid4

from phound.events import EventType, ChatType
from phound.event_listener import EventListener
from phound.server import Server, Connection
from phound.client import Client
from phound.handlers import BaseChatHandler, BaseCallHandler
from phound.logging import logger
from phound.chats.utils import get_chat_id, parse_attachments, guess_text_format, extract_mentions
from phound.chats.text_helpers import MessageTextFormat


class Phound:
    def __init__(self) -> None:
        self._server = Server()
        self._client = Client()
        self._chat_handlers: List[Tuple[BaseChatHandler, List[ChatType]]] = []
        self._call_handlers: List[BaseCallHandler] = []
        self._channel_threads: Set[threading.Thread] = set()

    def __enter__(self) -> "Phound":
        return self

    def __exit__(self, *args: Any) -> None:
        self.stop()

    def send_message(
        self,
        text: str,
        from_persona_uid: str,
        chat_id: str = "",
        persona_uid: str = "",
        text_format: Optional[MessageTextFormat] = None,
        attachments: Optional[List[str]] = None,
        app_meta: Optional[Dict[str, Any]] = None
    ) -> None:
        to_chat_id = chat_id if chat_id else get_chat_id(from_persona_uid, persona_uid)
        text_format = text_format or guess_text_format(text)
        text, mentions = extract_mentions(text, text_format)
        self._client.send_message(from_persona_uid,
                                  to_chat_id,
                                  text,
                                  text_format=text_format,
                                  attachments=parse_attachments(attachments) if attachments else None,
                                  mentions=mentions,
                                  app_meta=app_meta)

    def register_chat_handler(
        self, handler: BaseChatHandler, chat_types: Tuple[str, ...] = (ChatType.PRIVATE,)
    ) -> None:
        self._chat_handlers.append((handler, [ChatType(chat_type) for chat_type in chat_types]))

    def register_call_handler(self, handler: BaseCallHandler) -> None:
        self._call_handlers.append(handler)

    def stop(self) -> None:
        logger.info("Gracefully stopping phound")
        self._client.shutdown()
        for t in self._channel_threads:
            t.join()
        self._client.stop()

    def start_listen_events(self) -> None:
        self._client.enable_channels(self._server.port)
        try:
            while True:
                # updating alive threads here is not ideal but seems optimal for now
                self._channel_threads = {t for t in self._channel_threads if t.is_alive()}
                conn = self._server.get_new_connection()
                logger.info(f"Got new connection: {conn}")
                thread = threading.Thread(target=self._start_listen_connection, args=(conn,), name=str(uuid4()))
                self._channel_threads.add(thread)
                thread.start()
        except KeyboardInterrupt:
            logger.info("Ctrl+C pressed, stopping listen events")

    def _start_listen_connection(self, conn: Connection) -> None:
        event_listener = EventListener(conn.file)
        channel = event_listener.wait_event(EventType.NEW_CHANNEL).body
        logger.info(f"Channel: {channel}")

        self._client.request_next_event(channel.id)
        start_event = event_listener.wait_event(accept_any=True)
        logger.info(f"Start event: {start_event}")
        if start_event.type == EventType.CHAT_MESSAGE:
            cls_chat_handler = next((h[0] for h in self._chat_handlers if start_event.body.chat_type in h[1]), None)
            if cls_chat_handler:
                try:
                    chat = cls_chat_handler(start_event.body.chat_id,
                                            start_event.body.persona_uid,
                                            start_event.body.chat_type,
                                            channel.id,
                                            conn,
                                            self._client)
                    chat.start(start_event)
                except Exception as e:
                    logger.error(e, exc_info=True)
        elif start_event.type == EventType.CALL_INCOMING:
            cls_call_handler = next((h for h in self._call_handlers), None)
            if cls_call_handler:
                try:
                    call = cls_call_handler(start_event.body.id,
                                            start_event.body.persona_uid,
                                            channel.id,
                                            conn,
                                            self._client)
                    call.start(start_event)
                except Exception as e:
                    logger.error(e, exc_info=True)

        conn.close()
