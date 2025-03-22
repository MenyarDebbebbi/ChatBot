from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import json
import os
from .text_processor import TextProcessor

class ChatbotClassifier:
    def __init__(self, text_processor=None):
        # Initialisation du classificateur KNN
        self.knn = KNeighborsClassifier(
            n_neighbors=3,
            weights='distance'
        )
        
        # Initialisation du processeur de texte
        self.text_processor = text_processor if text_processor else TextProcessor()
        
        # Chargement des données
        self.load_training_data()
        
        # Prétraitement et entraînement initial
        self.prepare_and_train()
        
    def prepare_and_train(self):
        """Préparation des données et entraînement des modèles"""
        try:
            # Prétraitement des questions
            processed_questions = [
                self.text_processor.preprocess(q) 
                for q in self.questions
            ]
            
            # Entraînement des vectorizers
            self.text_processor.fit_vectorizers(processed_questions)
            
            # Vectorisation des questions
            X = self.text_processor.get_tfidf_vectors(processed_questions)
            
            # Entraînement du modèle KNN
            self.knn.fit(X, self.responses)
            
            print("Entraînement du modèle terminé avec succès!")
            
        except Exception as e:
            print(f"Erreur lors de la préparation et de l'entraînement : {e}")
            raise e
    
    def load_training_data(self):
        try:
            # Charger les données d'entraînement
            data_path = os.path.join('data', 'training_data.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Vérifier que le nombre de questions et réponses correspond
            self.questions = data['questions']
            self.responses = data['responses']
            
            if len(self.questions) != len(self.responses):
                print(f"Erreur: Nombre de questions ({len(self.questions)}) différent du nombre de réponses ({len(self.responses)})")
                # Utiliser uniquement les paires complètes
                min_len = min(len(self.questions), len(self.responses))
                self.questions = self.questions[:min_len]
                self.responses = self.responses[:min_len]
            
            print(f"Données chargées avec succès! ({len(self.questions)} paires question-réponse)")
            
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            # Données par défaut minimales
            self.questions = ["Bonjour", "Au revoir"]
            self.responses = ["Bonjour! Comment puis-je vous aider?", "Au revoir! Bonne journée!"]
    
    def get_response(self, question):
        try:
            # Prétraitement de la question
            processed_question = self.text_processor.preprocess(question)
            
            # Vectorisation
            question_vector = self.text_processor.get_tfidf_vectors([processed_question])
            
            # Utilisation de KNN pour trouver les questions similaires et la réponse
            distances, indices = self.knn.kneighbors(question_vector)
            
            # Calcul du score de confiance basé sur la distance
            confidence = 1 / (1 + distances[0][0])
            
            # Sélection de la réponse la plus proche
            response = self.responses[indices[0][0]]
            
            # Récupération des questions similaires
            similar_questions = [self.questions[i] for i in indices[0]]
            
            result = {
                'response': response,
                'confidence': float(confidence),  # Conversion en float pour la sérialisation JSON
                'similar_questions': similar_questions
            }
            
            return result
            
        except Exception as e:
            print(f"Erreur lors de la génération de réponse : {e}")
            return {
                'response': "Désolé, je n'ai pas compris votre question. Pouvez-vous la reformuler ?",
                'confidence': 0.0,
                'similar_questions': []
            } 