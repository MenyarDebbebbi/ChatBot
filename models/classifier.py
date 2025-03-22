from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import json
import os

class ChatbotClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = KNeighborsClassifier(n_neighbors=5)
        self.load_training_data()
        
    def load_training_data(self):
        try:
            # Charger les données d'entraînement
            data_path = os.path.join('data', 'training_data.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Entraîner le vectorizer et le classifier
            questions = data['questions']
            responses = data['responses']
            
            # Vectorisation et entraînement
            X = self.vectorizer.fit_transform(questions)
            self.classifier.fit(X, responses)
            
            print("Modèle entraîné avec succès!")
            
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            # Données par défaut au cas où
            default_questions = ["Bonjour", "Au revoir"]
            default_responses = ["Bonjour! Comment puis-je vous aider?", "Au revoir!"]
            X = self.vectorizer.fit_transform(default_questions)
            self.classifier.fit(X, default_responses)
    
    def get_response(self, question):
        try:
            # Vectorisation de la question
            X = self.vectorizer.transform([question])
            
            # Prédiction
            response = self.classifier.predict(X)[0]
            
            # Calcul du score de confiance
            distances, indices = self.classifier.kneighbors(X)
            confidence = 1 / (1 + distances[0][0])
            
            return response, confidence
            
        except Exception as e:
            print(f"Erreur lors de la génération de réponse : {e}")
            return "Désolé, je n'ai pas compris votre question.", 0.0 