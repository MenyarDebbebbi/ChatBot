import json
import os
from typing import Dict, List, Union, Optional

class CombinedDataManager:
    def __init__(self, scraping_file: str = 'data/scraping-data.json', training_file: str = 'data/training_data.json'):
        """Initialise le gestionnaire avec les deux sources de données."""
        self.scraped_data = {}
        self.training_data = []
        
        # Charger les données scrapées si le fichier existe
        if os.path.exists(scraping_file):
            try:
                with open(scraping_file, 'r', encoding='utf-8') as f:
                    self.scraped_data = json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de {scraping_file}: {e}")
        
        # Charger les données d'entraînement si le fichier existe
        if os.path.exists(training_file):
            try:
                with open(training_file, 'r', encoding='utf-8') as f:
                    self.training_data = json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de {training_file}: {e}")
        
        # Si les données d'entraînement n'existent pas, créer des données par défaut
        if not self.training_data:
            self.training_data = [
                {
                    "patterns": [
                        "Quels sont les programmes disponibles ?",
                        "Quelles formations sont disponibles ?",
                        "Quels sont les cursus disponibles ?",
                        "Que peut-on étudier à l'ISET ?"
                    ],
                    "responses": [
                        "L'ISET Sfax propose les formations suivantes :\n\n1. Licence Nationale en Technologies de l'Informatique :\n- Formation initiale et à distance\n- Spécialisation en développement logiciel, réseaux et systèmes informatiques\n\n2. Mastères Professionnels :\n- Administration des Systèmes, Sécurité et Cloud Computing (ASSCC)\n- Développement des Systèmes Informatiques et Réseaux (DSIR)"
                    ]
                },
                {
                    "patterns": [
                        "Comment s'inscrire à l'ISET ?",
                        "Quelle est la procédure d'inscription ?",
                        "Je veux m'inscrire à l'ISET",
                        "Comment faire pour s'inscrire ?"
                    ],
                    "responses": [
                        "Pour s'inscrire à l'ISET Sfax, voici la procédure à suivre :\n\n1. Inscription en ligne sur le site www.orientation.tn\n2. Dépôt du dossier d'inscription comprenant :\n   - Extrait de naissance\n   - Copie de la CIN\n   - 4 photos d'identité\n   - Relevé de notes du bac\n   - Reçu des frais d'inscription\n3. Validation de l'inscription au bureau de scolarité\n\nPour plus d'informations, contactez le service de scolarité au (+216) 74 431 425"
                    ]
                }
            ]
            
            # Sauvegarder les données d'entraînement par défaut
            os.makedirs(os.path.dirname(training_file), exist_ok=True)
            with open(training_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_data, f, ensure_ascii=False, indent=4)

    def get_training_response(self, query: str) -> Optional[str]:
        """Recherche une réponse dans les données d'entraînement."""
        query = query.lower()
        best_match = None
        highest_score = 0

        for item in self.training_data:
            for pattern in item['patterns']:
                if pattern.lower() in query or query in pattern.lower():
                    score = len(set(query.split()) & set(pattern.lower().split()))
                    if score > highest_score:
                        highest_score = score
                        best_match = item['responses']

        if best_match:
            return best_match[0] if isinstance(best_match, list) else best_match
        return None

    def get_course_info(self, course_name: str) -> Optional[Dict]:
        """Recherche les informations d'un cours spécifique."""
        # Recherche dans les données scrapées
        for semester in self.scraped_data['formations']['licence']['cours'].values():
            for course in semester:
                if course_name.lower() in course['nom'].lower():
                    return course
        
        # Recherche dans les cours UVT
        if 'ressources_uvt' in self.scraped_data:
            for category in self.scraped_data['ressources_uvt']['cours_informatiques']:
                for course in category['cours']:
                    if course_name.lower() in course['titre'].lower():
                        return course
        
        return None

    def get_stage_info(self, stage_type: str = None) -> Union[Dict, List[Dict]]:
        """Récupère les informations sur les stages."""
        if stage_type:
            for stage in self.scraped_data['stages']['types']:
                if stage_type.lower() in stage['nom'].lower():
                    return stage
            return None
        return self.scraped_data['stages']

    def get_attestation_info(self, attestation_type: str = None) -> Union[Dict, List[Dict]]:
        """Récupère les informations sur les attestations."""
        if attestation_type:
            for attestation in self.scraped_data['documents_administratifs']['attestations']:
                if attestation_type.lower() in attestation['type'].lower():
                    return attestation
            return None
        return self.scraped_data['documents_administratifs']

    def get_teacher_info(self, teacher_name: str = None) -> Union[Dict, List[Dict]]:
        """Récupère les informations sur les enseignants."""
        if teacher_name:
            for teacher in self.scraped_data['enseignants']:
                if teacher_name.lower() in teacher['nom'].lower():
                    return teacher
            return None
        return self.scraped_data['enseignants']

    def search_all_content(self, query: str) -> Dict:
        """Recherche dans toutes les sources de données."""
        results = {
            "training_response": self.get_training_response(query),
            "scraped_data": {
                "cours": [],
                "stages": [],
                "attestations": [],
                "enseignants": [],
                "ressources": []
            }
        }

        # Recherche dans les cours
        for semester in self.scraped_data['formations']['licence']['cours'].values():
            for course in semester:
                if query.lower() in str(course).lower():
                    results["scraped_data"]["cours"].append(course)

        # Recherche dans les stages
        for stage in self.scraped_data['stages']['types']:
            if query.lower() in str(stage).lower():
                results["scraped_data"]["stages"].append(stage)

        # Recherche dans les attestations
        for attestation in self.scraped_data['documents_administratifs']['attestations']:
            if query.lower() in str(attestation).lower():
                results["scraped_data"]["attestations"].append(attestation)

        # Recherche dans les enseignants
        for teacher in self.scraped_data['enseignants']:
            if query.lower() in str(teacher).lower():
                results["scraped_data"]["enseignants"].append(teacher)

        # Recherche dans les ressources UVT
        if 'ressources_uvt' in self.scraped_data:
            for category in self.scraped_data['ressources_uvt']['cours_informatiques']:
                for course in category['cours']:
                    if query.lower() in str(course).lower():
                        results["scraped_data"]["ressources"].append(course)

        return results

    def get_formation_info(self, formation_type: str = None) -> Dict:
        """Récupère les informations sur les formations."""
        if formation_type:
            if formation_type.lower() == 'licence':
                return self.scraped_data['formations']['licence']
            elif formation_type.lower() == 'mastere':
                return self.scraped_data['formations']['masteres']
        return self.scraped_data['formations'] 