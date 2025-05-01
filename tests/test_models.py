import unittest
import json
import os
from models.nlp_processor import NLPProcessor
from models.response_generator import ResponseGenerator

class TestNLPProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Créer un fichier de test temporaire
        cls.test_data = {
            "stages": {
                "questions": ["Comment faire un stage?"],
                "responses": {
                    "default": {
                        "text": "Voici la procédure de stage",
                        "steps": ["Étape 1", "Étape 2"]
                    }
                }
            }
        }
        with open('test_training_data.json', 'w', encoding='utf-8') as f:
            json.dump(cls.test_data, f)
        cls.nlp = NLPProcessor('test_training_data.json')

    def test_preprocess_text(self):
        text = "Comment faire un stage à l'ISET?"
        tokens = self.nlp.preprocess_text(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)

    def test_detect_category_and_intent(self):
        text = "Comment faire un stage?"
        category, match, score = self.nlp.detect_category_and_intent(text)
        self.assertEqual(category, "stages")
        self.assertGreater(score, 0.4)

    def test_analyze_sentiment(self):
        text = "Je suis très content de cette formation"
        sentiment = self.nlp.analyze_sentiment(text)
        self.assertEqual(sentiment, "positif")

    @classmethod
    def tearDownClass(cls):
        # Nettoyer les fichiers temporaires
        if os.path.exists('test_training_data.json'):
            os.remove('test_training_data.json')

class TestResponseGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Créer des données de test
        cls.test_data = {
            "stages": {
                "questions": ["Comment faire un stage?"],
                "responses": {
                    "default": {
                        "text": "Voici la procédure de stage",
                        "steps": ["Étape 1", "Étape 2"]
                    }
                }
            }
        }
        with open('test_training_data.json', 'w', encoding='utf-8') as f:
            json.dump(cls.test_data, f)
        cls.generator = ResponseGenerator('test_training_data.json')

    def test_generate_response(self):
        response = self.generator.generate_response("Comment faire un stage?")
        self.assertIsInstance(response, dict)
        self.assertIn("text", response)

    def test_get_contextual_response(self):
        response = self.generator.get_contextual_response("stages")
        self.assertIsInstance(response, dict)
        self.assertIn("text", response)

    @classmethod
    def tearDownClass(cls):
        # Nettoyer les fichiers temporaires
        if os.path.exists('test_training_data.json'):
            os.remove('test_training_data.json')

if __name__ == '__main__':
    unittest.main() 