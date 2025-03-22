import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re

class TextProcessor:
    def __init__(self):
        try:
            self.stemmer = SnowballStemmer('french')
            self.stop_words = set(stopwords.words('french'))
        except LookupError:
            print("Téléchargement des ressources NLTK nécessaires...")
            nltk.download('punkt')
            nltk.download('stopwords')
            self.stemmer = SnowballStemmer('french')
            self.stop_words = set(stopwords.words('french'))
        
    def preprocess(self, text):
        # Conversion en minuscules
        text = text.lower()
        
        # Suppression des caractères spéciaux
        text = re.sub(r'[^\w\s]', '', text)
        
        try:
            # Tokenization
            tokens = word_tokenize(text)
            
            # Suppression des stop words et stemming
            tokens = [self.stemmer.stem(token) for token in tokens 
                     if token not in self.stop_words]
            
            return ' '.join(tokens)
        except Exception as e:
            print(f"Erreur lors du prétraitement : {e}")
            return text 