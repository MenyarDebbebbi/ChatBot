from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import json
import os

class ChatbotClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            min_df=1,
            ngram_range=(1, 2),
            strip_accents='unicode'
        )
        self.classifier = KNeighborsClassifier(
            n_neighbors=3,
            weights='distance'
        )
        self.load_training_data()
        
    def load_training_data(self):
        try:
            # Charger les données d'entraînement
            data_path = os.path.join('data', 'training_data.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Vérifier que le nombre de questions et réponses correspond
            questions = data['questions']
            responses = data['responses']
            
            if len(questions) != len(responses):
                print(f"Erreur: Nombre de questions ({len(questions)}) différent du nombre de réponses ({len(responses)})")
                # Utiliser uniquement les paires complètes
                min_len = min(len(questions), len(responses))
                questions = questions[:min_len]
                responses = responses[:min_len]
            
            # Vectorisation et entraînement
            X = self.vectorizer.fit_transform(questions)
            self.classifier.fit(X, responses)
            
            print(f"Modèle entraîné avec succès! ({len(questions)} paires question-réponse)")
            
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            # Données par défaut minimales
            questions = ["Bonjour", "Au revoir"]
            responses = ["Bonjour! Comment puis-je vous aider?", "Au revoir! Bonne journée!"]
            X = self.vectorizer.fit_transform(questions)
            self.classifier.fit(X, responses)
    
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
            return "Désolé, je n'ai pas compris votre question. Pouvez-vous la reformuler ?", 0.0 