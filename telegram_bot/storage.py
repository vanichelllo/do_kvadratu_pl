from typing import Any, Mapping

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, DefaultKeyBuilder, StateType, StorageKey
from asgiref.sync import sync_to_async
from django.db import close_old_connections

from .models import BotFSMState


class DjangoStorage(BaseStorage):
    """Сховище станів aiogram у базі даних: квіз і анкета не губляться після перезапуску
    сервера і працюють при кількох процесах gunicorn."""

    def __init__(self):
        self.key_builder = DefaultKeyBuilder(with_bot_id=True, with_destiny=True)

    def _key(self, key: StorageKey) -> str:
        return self.key_builder.build(key)

    @staticmethod
    @sync_to_async
    def _get(db_key):
        close_old_connections()  # потік sync_to_async живе довго — прибираємо «мертві» з'єднання
        return BotFSMState.objects.filter(key=db_key).values('state', 'data').first()

    @staticmethod
    @sync_to_async
    def _set(db_key, **fields):
        close_old_connections()
        BotFSMState.objects.update_or_create(key=db_key, defaults=fields)

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        value = state.state if isinstance(state, State) else state
        await self._set(self._key(key), state=value)

    async def get_state(self, key: StorageKey) -> str | None:
        row = await self._get(self._key(key))
        return row['state'] if row else None

    async def set_data(self, key: StorageKey, data: Mapping[str, Any]) -> None:
        await self._set(self._key(key), data=dict(data))

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        row = await self._get(self._key(key))
        return dict(row['data']) if row and row['data'] else {}

    async def close(self) -> None:
        pass
