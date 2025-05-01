class ModelConfig:
    # Configuration NLP
    NLP_CONFIG = {
        'language': 'french',
        'min_word_length': 3,
        'max_keywords': 5,
        'similarity_threshold': 0.4,
        'sentiment_threshold': 0.5
    }
    
    # Configuration des chemins
    PATHS = {
        'attestations': 'web/static/images/attestations/',
        'responses': 'data/responses.json',
        'training': 'data/training_data.json',
        'models': 'models/trained/',
        'logs': 'logs/'
    }
    
    # Configuration des types de réponses
    RESPONSE_TYPES = [
        'text',
        'image',
        'suggestions',
        'steps',
        'links'
    ]
    
    # Types d'attestations supportés
    ATTESTATION_TYPES = {
        'travail': {
            'extension': '.jpg',
            'required_fields': ['nom', 'date', 'poste']
        },
        'stage': {
            'extension': '.jpg',
            'required_fields': ['nom', 'date', 'entreprise']
        }
    }
    
    # Configuration des intentions
    INTENT_CONFIG = {
        'threshold': 0.4,
        'default_intent': 'autre',
        'supported_intents': [
            'salutation',
            'question',
            'demande_aide',
            'remerciement',
            'attestation',
            'inscription',
            'information'
        ]
    }
    
    # Configuration des entités
    ENTITY_TYPES = [
        'noms',
        'verbes',
        'adjectifs'
    ]
    
    SUPPORTED_ENTITIES = {
        'noms': [
            'attestation',
            'stage',
            'travail',
            'formation',
            'cours',
            'examen'
        ],
        'verbes': [
            'vouloir',
            'faire',
            'obtenir',
            'demander',
            'passer'
        ],
        'adjectifs': [
            'disponible',
            'possible',
            'urgent',
            'important'
        ]
    }
    
    # Messages d'erreur
    ERROR_MESSAGES = {
        'not_found': "Désolé, je n'ai pas trouvé l'information demandée.",
        'invalid_request': "Je ne comprends pas votre demande. Pourriez-vous la reformuler ?",
        'processing_error': "Une erreur est survenue lors du traitement de votre demande.",
        'missing_data': "Des informations sont manquantes pour traiter votre demande."
    }
    
    # Configuration de journalisation
    ENABLE_LOGGING = True
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'chatbot.log' 