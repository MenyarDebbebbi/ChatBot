import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim.models import FastText
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re

class TextProcessor:
    def __init__(self):
        try:
            # Initialisation des composants NLTK
            self.stemmer = SnowballStemmer('french')
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('french'))
            
            # Téléchargement des ressources NLTK nécessaires
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
            
            # Initialisation des vectorizers
            self.tfidf_vectorizer = TfidfVectorizer(
                min_df=1,
                ngram_range=(1, 2),
                strip_accents='unicode'
            )
            self.bow_vectorizer = CountVectorizer(
                min_df=1,
                ngram_range=(1, 2),
                strip_accents='unicode'
            )
            
            # Initialisation du modèle FastText (sera entraîné plus tard)
            self.fasttext_model = None
            
        except LookupError:
            print("Téléchargement des ressources NLTK nécessaires...")
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
            self.stemmer = SnowballStemmer('french')
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('french'))
    
    def tokenize(self, text):
        """Tokenisation du texte"""
        return word_tokenize(text.lower())
    
    def remove_stopwords(self, tokens):
        """Suppression des stop words"""
        return [token for token in tokens if token not in self.stop_words]
    
    def stem_words(self, tokens):
        """Application du stemming"""
        return [self.stemmer.stem(token) for token in tokens]
    
    def lemmatize_words(self, tokens):
        """Application de la lemmatisation"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text, use_lemmatization=False):
        """Prétraitement complet du texte"""
        # Conversion en minuscules et nettoyage
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenisation
        tokens = self.tokenize(text)
        
        # Suppression des stop words
        tokens = self.remove_stopwords(tokens)
        
        # Application du stemming ou de la lemmatisation
        if use_lemmatization:
            tokens = self.lemmatize_words(tokens)
        else:
            tokens = self.stem_words(tokens)
        
        return ' '.join(tokens)
    
    def fit_vectorizers(self, texts):
        """Entraînement des vectorizers sur un corpus de textes"""
        # Entraînement TF-IDF
        self.tfidf_vectorizer.fit(texts)
        
        # Entraînement BoW
        self.bow_vectorizer.fit(texts)
        
        # Entraînement FastText
        self.train_fasttext(texts)
    
    def get_tfidf_vectors(self, texts):
        """Conversion en vecteurs TF-IDF"""
        return self.tfidf_vectorizer.transform(texts)
    
    def get_bow_vectors(self, texts):
        """Conversion en vecteurs BoW"""
        return self.bow_vectorizer.transform(texts)
    
    def train_fasttext(self, texts, vector_size=100, window=5, min_count=1):
        """Entraînement du modèle FastText"""
        # Préparation des données pour FastText
        tokenized_texts = [text.split() for text in texts]
        self.fasttext_model = FastText(
            tokenized_texts,
            vector_size=vector_size,
            window=window,
            min_count=min_count
        )
    
    def get_fasttext_vector(self, text):
        """Obtention du vecteur FastText pour un texte"""
        if self.fasttext_model is None:
            raise ValueError("Le modèle FastText n'a pas été entraîné")
        
        words = text.split()
        word_vectors = [self.fasttext_model.wv[word] for word in words if word in self.fasttext_model.wv]
        
        if not word_vectors:
            return np.zeros(self.fasttext_model.vector_size)
        
        return np.mean(word_vectors, axis=0)
    
    def compute_cosine_similarity(self, vec1, vec2):
        """Calcul de la similarité cosinus entre deux vecteurs"""
        return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
    
    def validate_question(self, text):
        """Validation et nettoyage basique de la question"""
        # Nettoyage basique
        text = text.strip().lower()
        
        # Vérifier la longueur minimale
        if len(text) < 2:
            return False, "La question est trop courte"
        
        # Prétraitement de la question
        processed_text = self.preprocess(text)
        
        return True, processed_text 