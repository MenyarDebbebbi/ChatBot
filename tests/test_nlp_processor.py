import unittest
import json
import os
from models.nlp_processor import NLPProcessor

class TestNLPProcessor(unittest.TestCase):
    def setUp(self):
        # Créer des données de test temporaires
        self.test_data = {
            "stages": {
                "questions": [
                    "Comment faire une demande de stage?",
                    "Quelles sont les conditions pour un stage?"
                ],
                "responses": {
                    "default": "Pour faire une demande de stage, suivez ces étapes..."
                }
            },
            "attestations": {
                "questions": [
                    "Je voudrais une attestation de travail",
                    "Comment obtenir une attestation?"
                ],
                "responses": {
                    "default": "Pour obtenir une attestation..."
                }
            }
        }
        
        # Créer un fichier temporaire pour les données de test
        self.test_file = "test_training_data.json"
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.test_data, f, ensure_ascii=False)
            
        self.nlp = NLPProcessor(self.test_file)

    def tearDown(self):
        # Nettoyer les fichiers temporaires
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_preprocess_text(self):
        text = "Je voudrais faire une demande de stage"
        processed = self.nlp.preprocess_text(text)
        self.assertIsInstance(processed, str)
        self.assertTrue(len(processed) > 0)

    def test_calculate_similarity(self):
        text1 = "demande de stage"
        text2 = "faire une demande de stage"
        similarity = self.nlp.calculate_similarity(text1, text2)
        self.assertIsInstance(similarity, float)
        self.assertTrue(0 <= similarity <= 1)

    def test_find_best_match(self):
        input_text = "Comment faire pour un stage?"
        category = "stages"
        best_match, score = self.nlp.find_best_match(input_text, self.test_data[category]["questions"])
        self.assertIsInstance(best_match, str)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 1)

    def test_detect_category_and_intent(self):
        input_text = "Je voudrais faire un stage"
        category, intent, score = self.nlp.detect_category_and_intent(input_text)
        self.assertEqual(category, "stages")
        self.assertIsInstance(intent, str)
        self.assertIsInstance(score, float)

    def test_extract_entities(self):
        text = "Je voudrais une attestation de travail pour mon stage"
        entities = self.nlp.extract_entities(text)
        self.assertIsInstance(entities, dict)
        self.assertTrue("nouns" in entities)
        self.assertTrue("verbs" in entities)
        self.assertTrue("adjectives" in entities)

    def test_analyze_sentiment(self):
        positive_text = "Je suis très content de votre service"
        negative_text = "Je suis déçu de la réponse"
        
        positive_score = self.nlp.analyze_sentiment(positive_text)
        negative_score = self.nlp.analyze_sentiment(negative_text)
        
        self.assertIsInstance(positive_score, float)
        self.assertIsInstance(negative_score, float)
        self.assertTrue(positive_score > negative_score)

    def test_get_response_for_category(self):
        category = "stages"
        entities = {"nouns": ["stage"], "verbs": ["faire"], "adjectives": []}
        response = self.nlp.get_response_for_category(category, entities)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_unknown_category(self):
        input_text = "Quelque chose de complètement différent"
        category, intent, score = self.nlp.detect_category_and_intent(input_text)
        self.assertTrue(score < self.nlp.config.INTENT_THRESHOLD)

if __name__ == '__main__':
    unittest.main() 