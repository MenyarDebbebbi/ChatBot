import json
import random
from datetime import datetime
from .nlp_processor import NLPProcessor

class ResponseGenerator:
    def __init__(self, training_data_file='data/training_data.json'):
        self.nlp = NLPProcessor(training_data_file)
        
    def generate_response(self, user_input):
        """Génère une réponse basée sur l'entrée utilisateur."""
        # Détection de la catégorie et de l'intention
        category, matched_question, confidence = self.nlp.detect_category_and_intent(user_input)
        
        # Si aucune catégorie n'est trouvée avec suffisamment de confiance
        if not category or confidence < 0.4:
            return {
                "text": "Je ne suis pas sûr de comprendre votre demande. Pourriez-vous la reformuler ou choisir parmi ces sujets :",
                "suggestions": ["Stages", "Attestations", "Inscription", "Formations", "Examens"]
            }
        
        # Extraction des entités pour une réponse plus précise
        entities = self.nlp.extract_entities(user_input)
        
        # Analyse du sentiment pour adapter la réponse
        sentiment = self.nlp.analyze_sentiment(user_input)
        
        # Obtention de la réponse appropriée
        response = self.nlp.get_response_for_category(category, entities)
        
        # Si aucune réponse spécifique n'est trouvée
        if not response:
            return {
                "text": "Je n'ai pas trouvé de réponse spécifique. Voici les informations générales sur ce sujet :",
                "category": category
            }
        
        # Ajout de suggestions pertinentes selon la catégorie
        if category == "stages":
            response["suggestions"] = [
                "Comment trouver un stage?",
                "Durée du stage",
                "Attestation de stage"
            ]
        elif category == "attestations":
            response["suggestions"] = [
                "Attestation de travail",
                "Attestation de stage",
                "Attestation de scolarité"
            ]
        
        return response
    
    def get_contextual_response(self, category, time=None):
        """Génère une réponse contextuelle basée sur l'heure."""
        if not time:
            time = datetime.now()
        
        hour = time.hour
        greeting = ""
        
        if 5 <= hour < 12:
            greeting = "Bonjour! "
        elif 12 <= hour < 18:
            greeting = "Bon après-midi! "
        else:
            greeting = "Bonsoir! "
            
        response = self.nlp.get_response_for_category(category)
        if isinstance(response, dict) and "text" in response:
            response["text"] = greeting + response["text"]
            
        return response
    
    def add_training_data(self, category, question, response):
        """Ajoute de nouvelles données d'entraînement."""
        if category in self.nlp.training_data:
            if question not in self.nlp.training_data[category]["questions"]:
                self.nlp.training_data[category]["questions"].append(question)
            
            if isinstance(response, dict):
                self.nlp.training_data[category]["responses"].update(response)
            
            # Sauvegarde des modifications
            with open('data/training_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.nlp.training_data, f, ensure_ascii=False, indent=2) 