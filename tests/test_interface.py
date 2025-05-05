import unittest
from flask import url_for
from app import app

class TestChatbotInterface(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test si la page d'accueil se charge correctement"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Assistant Virtuel ISET', response.data)

    def test_chatbot_page(self):
        """Test si la page du chatbot se charge correctement"""
        response = self.app.get('/chatbot')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'chat-container', response.data)

    def test_chat_endpoint(self):
        """Test l'endpoint de chat"""
        test_message = {"message": "Bonjour"}
        response = self.app.post('/chat', 
                               json=test_message,
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('response' in response.json)

    def test_voice_input(self):
        """Test si la fonction de reconnaissance vocale est présente"""
        response = self.app.get('/chatbot')
        self.assertIn(b'voice-button', response.data)
        self.assertIn(b'toggleVoiceInput', response.data)

    def test_suggestions(self):
        """Test si les suggestions sont présentes"""
        response = self.app.get('/chatbot')
        self.assertIn(b'suggested-questions', response.data)
        self.assertIn(b'Comment s\'inscrire', response.data)

    def test_health_endpoint(self):
        """Test l'endpoint de santé"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('version', data)

if __name__ == '__main__':
    unittest.main() 