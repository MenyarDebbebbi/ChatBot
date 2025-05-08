import json
from typing import Dict, List, Union, Optional

class ISETDataManager:
    def __init__(self, json_file: str = 'data/scraping-data.json'):
        """Initialise le gestionnaire de données avec le fichier JSON."""
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_course_info(self, course_name: str) -> Optional[Dict]:
        """Recherche les informations d'un cours spécifique."""
        # Recherche dans les cours de licence
        for semester in self.data['formations']['licence']['cours'].values():
            for course in semester:
                if course_name.lower() in course['nom'].lower():
                    return course
        
        # Recherche dans les cours UVT
        for category in self.data['ressources_uvt']['cours_informatiques']:
            for course in category['cours']:
                if course_name.lower() in course['titre'].lower():
                    return course
        
        return None

    def get_stage_info(self, stage_type: str = None) -> Union[Dict, List[Dict]]:
        """Récupère les informations sur les stages."""
        if stage_type:
            for stage in self.data['stages']['types']:
                if stage_type.lower() in stage['nom'].lower():
                    return stage
            return None
        return self.data['stages']

    def get_attestation_info(self, attestation_type: str = None) -> Union[Dict, List[Dict]]:
        """Récupère les informations sur les attestations."""
        if attestation_type:
            for attestation in self.data['documents_administratifs']['attestations']:
                if attestation_type.lower() in attestation['type'].lower():
                    return attestation
            return None
        return self.data['documents_administratifs']

    def get_teacher_info(self, teacher_name: str = None) -> Union[Dict, List[Dict]]:
        """Récupère les informations sur les enseignants."""
        if teacher_name:
            for teacher in self.data['enseignants']:
                if teacher_name.lower() in teacher['nom'].lower():
                    return teacher
            return None
        return self.data['enseignants']

    def get_resources_info(self, resource_type: str = None) -> Dict:
        """Récupère les informations sur les ressources pédagogiques."""
        if resource_type:
            if resource_type in self.data['ressources_pedagogiques']:
                return {resource_type: self.data['ressources_pedagogiques'][resource_type]}
            return None
        return self.data['ressources_pedagogiques']

    def search_content(self, query: str) -> Dict:
        """Recherche générale dans tout le contenu."""
        results = {
            "cours": [],
            "stages": [],
            "attestations": [],
            "enseignants": [],
            "ressources": []
        }

        # Recherche dans les cours
        for semester in self.data['formations']['licence']['cours'].values():
            for course in semester:
                if query.lower() in str(course).lower():
                    results["cours"].append(course)

        # Recherche dans les stages
        for stage in self.data['stages']['types']:
            if query.lower() in str(stage).lower():
                results["stages"].append(stage)

        # Recherche dans les attestations
        for attestation in self.data['documents_administratifs']['attestations']:
            if query.lower() in str(attestation).lower():
                results["attestations"].append(attestation)

        # Recherche dans les enseignants
        for teacher in self.data['enseignants']:
            if query.lower() in str(teacher).lower():
                results["enseignants"].append(teacher)

        # Recherche dans les ressources UVT
        if 'ressources_uvt' in self.data:
            for category in self.data['ressources_uvt']['cours_informatiques']:
                for course in category['cours']:
                    if query.lower() in str(course).lower():
                        results["ressources"].append(course)

        return results

    def get_formation_info(self, formation_type: str = None) -> Dict:
        """Récupère les informations sur les formations."""
        if formation_type:
            if formation_type.lower() == 'licence':
                return self.data['formations']['licence']
            elif formation_type.lower() == 'mastere':
                return self.data['formations']['masteres']
        return self.data['formations'] 