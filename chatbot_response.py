from models.combined_data_manager import CombinedDataManager

class ChatbotResponse:
    def __init__(self):
        self.data_manager = CombinedDataManager()

    def generate_response(self, user_query: str) -> str:
        """Génère une réponse en fonction de la requête de l'utilisateur."""
        # Convertir la requête en minuscules pour faciliter la comparaison
        query = user_query.lower()

        # D'abord, essayer de trouver une réponse dans les données d'entraînement
        training_response = self.data_manager.get_training_response(query)
        if training_response:
            return training_response

        # Si pas de réponse dans les données d'entraînement, chercher dans les données scrapées
        # Recherche d'informations sur les cours
        if any(keyword in query for keyword in ['cours', 'matière', 'module']):
            if 'algorithme' in query or 'algo' in query:
                course = self.data_manager.get_course_info('Algorithmes')
                if course:
                    return f"Voici les informations sur le cours d'Algorithmes :\n" \
                           f"- Nom: {course['nom']}\n" \
                           f"- Type: {course['type']}\n" \
                           f"- Crédits: {course['credits']}\n" \
                           f"- Ressources disponibles: {', '.join(course['ressources'].keys())}"

        # Recherche d'informations sur les stages
        if any(keyword in query for keyword in ['stage', 'pfe', 'initiation']):
            if 'pfe' in query:
                stage = self.data_manager.get_stage_info('PFE')
            elif 'initiation' in query:
                stage = self.data_manager.get_stage_info('initiation')
            else:
                stage = self.data_manager.get_stage_info()
            
            if isinstance(stage, dict) and 'nom' in stage:
                return f"Informations sur le {stage['nom']} :\n" \
                       f"- Durée: {stage['duree']}\n" \
                       f"- Période: {stage['periode']}\n" \
                       f"- Documents requis: {', '.join(stage['documents_requis'])}"

        # Recherche d'informations sur les attestations
        if any(keyword in query for keyword in ['attestation', 'document', 'certificat']):
            if 'présence' in query:
                attestation = self.data_manager.get_attestation_info('présence')
            elif 'réussite' in query:
                attestation = self.data_manager.get_attestation_info('réussite')
            else:
                attestations = self.data_manager.get_attestation_info()
                return "Types d'attestations disponibles :\n" + \
                       "\n".join([f"- {att['type']} (délai: {att['delai']})" 
                                 for att in attestations['attestations']])

        # Recherche d'informations sur les enseignants
        if any(keyword in query for keyword in ['professeur', 'enseignant', 'contact']):
            teachers = self.data_manager.get_teacher_info()
            return "Liste des enseignants :\n" + \
                   "\n".join([f"- {teacher['nom']} ({teacher['specialite']})\n  Email: {teacher['email']}" 
                             for teacher in teachers])

        # Si aucune correspondance spécifique n'est trouvée, effectuer une recherche générale
        results = self.data_manager.search_all_content(query)
        
        # Construire une réponse combinée
        response = ""
        
        # Ajouter la réponse des données d'entraînement si disponible
        if results["training_response"]:
            response += results["training_response"] + "\n\n"
        
        # Ajouter les résultats des données scrapées
        scraped_results = results["scraped_data"]
        if any(scraped_results.values()):
            if response:
                response += "J'ai aussi trouvé ces informations complémentaires :\n"
            else:
                response += "Voici ce que j'ai trouvé :\n"
                
            for category, items in scraped_results.items():
                if items:
                    response += f"\n{category.capitalize()}:\n"
                    for item in items:
                        if isinstance(item, dict):
                            response += f"- {item.get('nom', item.get('titre', 'Information trouvée'))}\n"
        
        if response:
            return response.strip()
        
        return "Je ne trouve pas d'information correspondant à votre demande. Pouvez-vous reformuler votre question ?"

    def format_response(self, response: str) -> str:
        """Formate la réponse pour un meilleur affichage."""
        return response.replace('\n', '<br>') 