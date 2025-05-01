import json
import random
from datetime import datetime
from .nlp_processor import NLPProcessor

class ResponseGenerator:
    def __init__(self, training_data_file='data/training_data.json'):
        self.nlp = NLPProcessor(training_data_file)
        self.load_responses()
        
    def load_responses(self):
        """Charge les réponses depuis le fichier responses.json"""
        try:
            with open('data/responses.json', 'r', encoding='utf-8') as f:
                self.responses = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des réponses: {e}")
            self.responses = {}

    def generate_response(self, user_input):
        """Génère une réponse basée sur l'entrée utilisateur."""
        user_input_lower = user_input.lower()
        
        # Détecter si c'est une demande d'attestation
        if "attestation" in user_input_lower:
            if "travail" in user_input_lower:
                return self.responses["attestation"]["travail"]
            elif "stage" in user_input_lower:
                return self.responses["attestation"]["stage"]
        
        # Détecter si c'est une demande sur les programmes
        if any(word in user_input_lower for word in ["programme", "formation", "étude", "spécialité"]):
            if "programmes" in self.responses:
                response = self.responses["programmes"]["default"].copy()
                # Formater la réponse pour inclure les détails des programmes
                programmes_text = []
                for prog in response["programmes"]:
                    prog_text = f"\n- {prog['nom']} : {prog['description']} (Durée : {prog['durée']})"
                    programmes_text.append(prog_text)
                response["text"] = response["text"] + "".join(programmes_text)
                return response
        
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
        
        # Pour les autres catégories
        if category in self.responses:
            if isinstance(self.responses[category], list):
                response = self.responses[category][0]
            elif isinstance(self.responses[category], dict):
                response = self.responses[category].get("default", {"text": "Je n'ai pas trouvé de réponse spécifique."})
            else:
                response = {"text": self.responses[category]}
        else:
            response = {
                "text": "Je n'ai pas trouvé de réponse spécifique. Voici les informations générales sur ce sujet :",
                "suggestions": ["Stages", "Attestations", "Inscription", "Formations"]
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
        elif category == "programmes" or category == "formations":
            response["suggestions"] = [
                "Comment s'inscrire à un programme ?",
                "Quelles sont les conditions d'admission ?",
                "Quels sont les débouchés ?"
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
            
        # Obtenir la réponse de base
        response = self.generate_response(category)
        
        # Ajouter le message de salutation
        if isinstance(response, dict) and "text" in response:
            response["text"] = greeting + response["text"]
        elif isinstance(response, str):
            response = {"text": greeting + response}
        
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