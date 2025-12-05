import json
import os

class ChatManager:
    def __init__(self, storage_file='chat_settings.json'):
        self.storage_file = storage_file
        self.allowed_chats = self._load_chats()

    def _load_chats(self):
        if not os.path.exists(self.storage_file):
            return []
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_chats(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.allowed_chats, f)

    def is_enabled(self, chat_id):
        return chat_id in self.allowed_chats

    def enable_chat(self, chat_id):
        if chat_id not in self.allowed_chats:
            self.allowed_chats.append(chat_id)
            self._save_chats()
            return True
        return False

    def disable_chat(self, chat_id):
        if chat_id in self.allowed_chats:
            self.allowed_chats.remove(chat_id)
            self._save_chats()
            return True
        return False
