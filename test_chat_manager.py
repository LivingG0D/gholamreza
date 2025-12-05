import unittest
import os
import json
from chat_manager import ChatManager

class TestChatManager(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_chat_settings.json'
        # Ensure we start with a clean slate
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        self.chat_manager = ChatManager(storage_file=self.test_file)

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_enable_chat(self):
        chat_id = 12345
        self.assertFalse(self.chat_manager.is_enabled(chat_id))
        
        result = self.chat_manager.enable_chat(chat_id)
        self.assertTrue(result)
        self.assertTrue(self.chat_manager.is_enabled(chat_id))

        # Test adding duplicate
        result = self.chat_manager.enable_chat(chat_id)
        self.assertFalse(result) # Should return False as it's already added

    def test_disable_chat(self):
        chat_id = 67890
        self.chat_manager.enable_chat(chat_id)
        self.assertTrue(self.chat_manager.is_enabled(chat_id))

        result = self.chat_manager.disable_chat(chat_id)
        self.assertTrue(result)
        self.assertFalse(self.chat_manager.is_enabled(chat_id))

        # Test removing non-existent
        result = self.chat_manager.disable_chat(chat_id)
        self.assertFalse(result)

    def test_persistence(self):
        chat_id = 11111
        self.chat_manager.enable_chat(chat_id)

        # Create a new instance to verify it loads from file
        new_manager = ChatManager(storage_file=self.test_file)
        self.assertTrue(new_manager.is_enabled(chat_id))

if __name__ == '__main__':
    unittest.main()
