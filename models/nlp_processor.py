import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import string
import re
import json
from difflib import SequenceMatcher

class NLPProcessor:
    def __init__(self, training_data_file='data/training_data.json'):
        # Télécharger les ressources NLTK nécessaires
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('french'))
        self.load_training_data(training_data_file)
        
    def load_training_data(self, file_path):
        """Charge les données d'entraînement depuis le fichier JSON."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.training_data = json.load(file)
        except FileNotFoundError:
            print(f"Attention: Fichier {file_path} non trouvé.")
            self.training_data = {}
    
    def preprocess_text(self, text):
        """Prétraite le texte pour l'analyse."""
        # Conversion en minuscules
        text = text.lower()
        
        # Suppression des caractères spéciaux et chiffres
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Suppression des stop words et lemmatization
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and token not in string.punctuation]
        
        return tokens
    
    def calculate_similarity(self, text1, text2):
        """Calcule la similarité entre deux textes."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def find_best_match(self, user_input, questions):
        """Trouve la meilleure correspondance parmi les questions d'entraînement."""
        best_match = None
        best_score = 0
        
        for question in questions:
            score = self.calculate_similarity(user_input, question)
            if score > best_score:
                best_score = score
                best_match = question
                
        return best_match, best_score
    
    def detect_category_and_intent(self, text):
        """Détecte la catégorie et l'intention spécifique du message."""
        best_category = None
        best_match = None
        best_score = 0
        
        for category, data in self.training_data.items():
            if 'questions' in data:
                match, score = self.find_best_match(text, data['questions'])
                if score > best_score:
                    best_score = score
                    best_match = match
                    best_category = category
        
        # Seuil de confiance minimum
        if best_score < 0.4:
            return None, None, best_score
            
        return best_category, best_match, best_score
    
    def extract_entities(self, text):
        """Extrait les entités nommées du texte."""
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        entities = {
            'noms': [],
            'verbes': [],
            'adjectifs': []
        }
        
        for word, tag in tagged:
            if tag.startswith('N'):  # Noms
                entities['noms'].append(word)
            elif tag.startswith('V'):  # Verbes
                entities['verbes'].append(word)
            elif tag.startswith('J'):  # Adjectifs
                entities['adjectifs'].append(word)
                
        return entities
    
    def analyze_sentiment(self, text):
        """Analyse le sentiment du texte."""
        # Liste de mots positifs et négatifs en français
        positive_words = {'merci', 'bien', 'super', 'excellent', 'parfait', 'content'}
        negative_words = {'mauvais', 'problème', 'erreur', 'difficile', 'impossible', 'nul'}
        
        tokens = self.preprocess_text(text)
        
        # Calcul du score de sentiment
        score = 0
        for token in tokens:
            if token in positive_words:
                score += 1
            elif token in negative_words:
                score -= 1
                
        # Détermination du sentiment
        if score > 0:
            return 'positif'
        elif score < 0:
            return 'négatif'
        else:
            return 'neutre'
    
    def get_response_for_category(self, category, entities=None):
        """Obtient la réponse appropriée pour une catégorie donnée."""
        if category not in self.training_data:
            return None
            
        category_data = self.training_data[category]
        
        # Gestion spéciale pour les attestations
        if category == 'attestations' and entities:
            for nom in entities.get('noms', []):
                if 'travail' in nom.lower():
                    return category_data['responses']['travail']
                elif 'stage' in nom.lower():
                    return category_data['responses']['stage']
                elif 'scolarite' in nom.lower():
                    return category_data['responses']['scolarite']
        
        # Retourne la réponse par défaut de la catégorie
        return category_data['responses'].get('default')
    
    def extract_keywords(self, text, top_n=5):
        """Extrait les mots-clés les plus importants du texte."""
        tokens = self.preprocess_text(text)
        
        # Calcul de la fréquence des mots
        word_freq = {}
        for token in tokens:
            word_freq[token] = word_freq.get(token, 0) + 1
            
        # Tri des mots par fréquence
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Retourne les top_n mots les plus fréquents
        return [word for word, freq in sorted_words[:top_n]]
    
    def detect_intent(self, text):
        """Détecte l'intention principale du message."""
        text = text.lower()
        
        # Définition des patterns d'intention
        intent_patterns = {
            'salutation': r'(bonjour|salut|hey|bonsoir|coucou)',
            'question': r'(comment|pourquoi|quand|où|qui|quoi|quel)',
            'demande_aide': r'(aide|besoin|support|assistance)',
            'remerciement': r'(merci|thanks|remercie)',
            'attestation': r'(attestation|certificat|document)',
            'inscription': r'(inscription|inscrire|candidature)',
            'information': r'(information|renseignement|détail)'
        }
        
        # Vérification des patterns
        for intent, pattern in intent_patterns.items():
            if re.search(pattern, text):
                return intent
                
        return 'autre' 