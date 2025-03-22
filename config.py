import os

class Config:
    # Chemins des fichiers
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Configuration Flask
    SECRET_KEY = 'votre-clé-secrète-ici'
    
    # Configuration du modèle
    SUPPORTED_LANGUAGES = ['fr', 'en']
    MIN_CONFIDENCE_SCORE = 0.7
    
    # Configuration du moteur de recherche
    SEARCH_INDEX_DIR = os.path.join(BASE_DIR, 'search_index')
    
    # Configuration des embeddings
    EMBEDDING_SIZE = 300
    EMBEDDING_MODEL = 'fasttext'  # ou 'word2vec', 'glove' 