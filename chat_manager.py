import json
import os


class ChatManager:
    """Manages allowed chat IDs with persistent JSON storage."""
    
    def __init__(self, storage_file='chat_settings.json'):
        self.storage_file = storage_file
        self._allowed_chats: set[int] = self._load_chats()

    def _load_chats(self) -> set[int]:
        """Load allowed chats from storage file."""
        if not os.path.exists(self.storage_file):
            return set()
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data) if isinstance(data, list) else set()
        except (json.JSONDecodeError, IOError):
            return set()

    def _save_chats(self) -> None:
        """Save allowed chats to storage file."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(list(self._allowed_chats), f)
        except IOError as e:
            print(f"Error saving chat settings: {e}")

    def is_enabled(self, chat_id: int) -> bool:
        """Check if a chat is enabled."""
        return chat_id in self._allowed_chats

    def enable_chat(self, chat_id: int) -> bool:
        """Enable a chat. Returns True if newly enabled, False if already enabled."""
        if chat_id not in self._allowed_chats:
            self._allowed_chats.add(chat_id)
            self._save_chats()
            return True
        return False

    def disable_chat(self, chat_id: int) -> bool:
        """Disable a chat. Returns True if disabled, False if wasn't enabled."""
        if chat_id in self._allowed_chats:
            self._allowed_chats.discard(chat_id)
            self._save_chats()
            return True
        return False
