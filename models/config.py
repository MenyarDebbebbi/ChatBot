class ModelConfig:
    # Configuration NLP
    NLP_CONFIG = {
        'language': 'french',
        'min_word_length': 3,
        'max_keywords': 5,
        'sentiment_threshold': 0.5
    }
    
    # Configuration des chemins
    PATHS = {
        'attestations': 'web/static/images/attestations/',
        'responses': 'data/responses.json',
        'models': 'models/trained/',
        'logs': 'logs/'
    }
    
    # Configuration des types de réponses
    RESPONSE_TYPES = {
        'text': True,
        'image': True,
        'suggestions': True,
        'links': True
    }
    
    # Types d'attestations supportés
    ATTESTATION_TYPES = {
        'travail': {
            'extensions': ['.jpg', '.pdf'],
            'required_fields': ['nom', 'date', 'poste']
        },
        'stage': {
            'extensions': ['.jpg', '.pdf'],
            'required_fields': ['nom', 'date', 'durée']
        }
    }
    
    # Configuration des intentions
    INTENT_CONFIG = {
        'threshold': 0.7,
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
    ENTITY_CONFIG = {
        'extract_names': True,
        'extract_dates': True,
        'extract_locations': True,
        'supported_entities': [
            'noms',
            'verbes',
            'adjectifs',
            'dates',
            'lieux'
        ]
    }
    
    # Messages d'erreur
    ERROR_MESSAGES = {
        'file_not_found': "Le fichier demandé n'a pas été trouvé.",
        'invalid_format': "Format de fichier non supporté.",
        'missing_fields': "Certains champs requis sont manquants.",
        'processing_error': "Une erreur est survenue lors du traitement.",
        'unknown_type': "Type d'attestation non reconnu."
    }
    
    # Configuration de journalisation
    LOGGING_CONFIG = {
        'enabled': True,
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'chatbot.log'
    } 