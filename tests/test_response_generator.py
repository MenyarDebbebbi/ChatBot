import unittest
import os
import json
from datetime import datetime
from models.response_generator import ResponseGenerator
from models.nlp_processor import NLPProcessor

class TestResponseGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Créer des données de test temporaires
        cls.test_data = {
            "stages": {
                "questions": [
                    "Comment faire une demande de stage?",
                    "Je voudrais faire un stage"
                ],
                "responses": {
                    "default": {
                        "text": "Pour faire une demande de stage, suivez ces étapes...",
                        "steps": ["Étape 1", "Étape 2"]
                    }
                }
            },
            "attestations": {
                "questions": [
                    "Je veux une attestation de travail",
                    "Attestation de stage svp"
                ],
                "responses": {
                    "travail": {
                        "text": "Voici votre attestation de travail",
                        "image": "/static/images/attestations/attestation_travail.jpg"
                    },
                    "stage": {
                        "text": "Voici votre attestation de stage",
                        "image": "/static/images/attestations/attestation_stage.jpg"
                    }
                }
            }
        }
        
        # Créer un fichier temporaire pour les données de test
        cls.test_file = "test_training_data.json"
        with open(cls.test_file, "w", encoding="utf-8") as f:
            json.dump(cls.test_data, f, ensure_ascii=False)
            
        cls.nlp = NLPProcessor(training_data_file=cls.test_file)
        cls.generator = ResponseGenerator(cls.test_file)

    @classmethod
    def tearDownClass(cls):
        # Nettoyer les fichiers temporaires
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    def test_generate_response(self):
        # Test pour une demande de stage
        input_text = "Je voudrais faire un stage"
        response = self.generator.generate_response(input_text)
        self.assertIsInstance(response, dict)
        self.assertIn("text", response)
        self.assertIn("suggestions", response)

        # Test pour une demande d'attestation
        input_text = "Je veux une attestation de travail"
        response = self.generator.generate_response(input_text)
        self.assertIsInstance(response, dict)
        self.assertIn("text", response)

    def test_get_contextual_response(self):
        # Test avec une heure spécifique du matin
        morning_time = datetime(2024, 1, 1, 9, 0)
        response = self.generator.get_contextual_response("stages", time=morning_time)
        self.assertIsInstance(response, dict)
        self.assertIn("text", response)
        self.assertTrue(response["text"].startswith("Bonjour!"))

        # Test avec une heure spécifique du soir
        evening_time = datetime(2024, 1, 1, 20, 0)
        response = self.generator.get_contextual_response("stages", time=evening_time)
        self.assertIsInstance(response, dict)
        self.assertIn("text", response)
        self.assertTrue(response["text"].startswith("Bonsoir!"))

    def test_add_training_data(self):
        category = "examens"
        question = "Quand sont les examens?"
        response = {
            "text": "Les examens commencent le 15 juin",
            "suggestions": ["Calendrier des examens", "Programme des révisions"]
        }
        
        self.generator.add_training_data(category, question, response)
        
        # Vérifier que les données ont été ajoutées en lisant le fichier
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertIn(category, data)
            self.assertIn(question, data[category]["questions"])
            self.assertEqual(
                data[category]["responses"]["default"]["text"],
                response["text"]
            )

    def test_generate_response_unknown_input(self):
        input_text = "XYZ123 ABC456"  # Texte sans sens
        response = self.generator.generate_response(input_text)
        self.assertIn("text", response)
        self.assertIn("suggestions", response)
        self.assertTrue(len(response["suggestions"]) > 0)

if __name__ == '__main__':
    unittest.main() 