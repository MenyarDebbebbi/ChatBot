import unittest
from models.config import ModelConfig

class TestModelConfig(unittest.TestCase):
    def setUp(self):
        self.config = ModelConfig()

    def test_nlp_config(self):
        self.assertEqual(self.config.NLP_CONFIG['language'], 'french')
        self.assertIsInstance(self.config.NLP_CONFIG['min_word_length'], int)
        self.assertIsInstance(self.config.NLP_CONFIG['max_keywords'], int)
        self.assertIsInstance(self.config.NLP_CONFIG['sentiment_threshold'], float)
        self.assertIsInstance(self.config.NLP_CONFIG['similarity_threshold'], float)

    def test_paths_config(self):
        self.assertIn('attestations', self.config.PATHS)
        self.assertIn('responses', self.config.PATHS)
        self.assertIn('training', self.config.PATHS)
        self.assertIn('models', self.config.PATHS)
        self.assertIn('logs', self.config.PATHS)

    def test_response_types(self):
        self.assertIsInstance(self.config.RESPONSE_TYPES, list)
        self.assertIn('text', self.config.RESPONSE_TYPES)
        self.assertIn('image', self.config.RESPONSE_TYPES)
        self.assertIn('suggestions', self.config.RESPONSE_TYPES)
        self.assertIn('steps', self.config.RESPONSE_TYPES)
        self.assertIn('links', self.config.RESPONSE_TYPES)

    def test_attestation_types(self):
        self.assertIsInstance(self.config.ATTESTATION_TYPES, dict)
        self.assertIn('travail', self.config.ATTESTATION_TYPES)
        self.assertIn('stage', self.config.ATTESTATION_TYPES)
        
        for att_type in ['travail', 'stage']:
            self.assertIn('extension', self.config.ATTESTATION_TYPES[att_type])
            self.assertIn('required_fields', self.config.ATTESTATION_TYPES[att_type])
            self.assertEqual(self.config.ATTESTATION_TYPES[att_type]['extension'], '.jpg')

    def test_intent_config(self):
        self.assertEqual(self.config.INTENT_CONFIG['threshold'], 0.4)
        self.assertEqual(self.config.INTENT_CONFIG['default_intent'], 'autre')
        self.assertIsInstance(self.config.INTENT_CONFIG['supported_intents'], list)
        self.assertIn('attestation', self.config.INTENT_CONFIG['supported_intents'])

    def test_entity_config(self):
        self.assertIsInstance(self.config.ENTITY_TYPES, list)
        self.assertIn('noms', self.config.ENTITY_TYPES)
        self.assertIn('verbes', self.config.ENTITY_TYPES)
        self.assertIn('adjectifs', self.config.ENTITY_TYPES)
        
        self.assertIsInstance(self.config.SUPPORTED_ENTITIES, dict)
        self.assertIn('noms', self.config.SUPPORTED_ENTITIES)
        self.assertIn('verbes', self.config.SUPPORTED_ENTITIES)
        self.assertIn('adjectifs', self.config.SUPPORTED_ENTITIES)

    def test_error_messages(self):
        self.assertIsInstance(self.config.ERROR_MESSAGES, dict)
        self.assertIn('not_found', self.config.ERROR_MESSAGES)
        self.assertIn('invalid_request', self.config.ERROR_MESSAGES)
        self.assertIn('processing_error', self.config.ERROR_MESSAGES)
        self.assertIn('missing_data', self.config.ERROR_MESSAGES)

    def test_logging_config(self):
        self.assertIsInstance(self.config.ENABLE_LOGGING, bool)
        self.assertEqual(self.config.LOG_LEVEL, 'INFO')
        self.assertEqual(self.config.LOG_FILE, 'chatbot.log')

if __name__ == '__main__':
    unittest.main() 