import json
import os
from typing import Dict, Union, Optional

class ResponseGenerator:
    def __init__(self):
        """Initialise le générateur de réponses"""
        print("Initialisation du ResponseGenerator...")
        self.training_data = self._load_training_data()
        self.scraped_data = self._load_scraped_data()
        print(f"Données d'entraînement chargées: {len(self.training_data)} entrées")
        print(f"Données scrapées chargées: {'Oui' if self.scraped_data else 'Non'}")

    def _load_training_data(self) -> list:
        """Charge les données d'entraînement"""
        default_data = [
            {
                "patterns": [
                    "bonjour", "salut", "bonsoir", "hello", "hi", "hey"
                ],
                "responses": [
                    "Bonjour ! Je suis le chatbot de l'ISET Sfax. Comment puis-je vous aider ?"
                ]
            },
            {
                "patterns": [
                    "au revoir", "bye", "à bientôt", "adieu", "ciao"
                ],
                "responses": [
                    "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions."
                ]
            },
            {
                "patterns": [
                    "merci", "thanks", "thank you", "je vous remercie"
                ],
                "responses": [
                    "Je vous en prie ! Je suis là pour vous aider."
                ]
            },
            {
                "patterns": [
                    "je veux accéder au cours php", "accès cours php", "comment accéder au cours php",
                    "je veux le cours php", "accéder php", "cours php accès"
                ],
                "responses": [
                    "Pour accéder au cours PHP, suivez ces étapes :\n\n1. Connectez-vous sur https://iset.uvt.tn\n2. Allez dans la section Technologies Web\n3. Sélectionnez le cours PHP/MySQL\n\nLien direct : https://iset.uvt.tn/course/view.php?id=104"
                ]
            },
            {
                "patterns": [
                    "je veux accéder au cours java", "accès cours java", "comment accéder au cours java",
                    "je veux le cours java", "accéder java", "cours java accès"
                ],
                "responses": [
                    "Pour accéder au cours Java, suivez ces étapes :\n\n1. Connectez-vous sur https://iset.uvt.tn\n2. Allez dans la section Programmation Orientée Objet\n3. Sélectionnez le cours Java\n\nLien direct : https://iset.uvt.tn/course/view.php?id=102"
                ]
            },
            {
                "patterns": [
                    "je veux accéder au cours javascript", "accès cours js", "comment accéder au cours javascript",
                    "je veux le cours js", "accéder javascript", "cours javascript accès", "cours js", "view js"
                ],
                "responses": [
                    "Pour accéder au cours JavaScript, suivez ces étapes :\n\n1. Connectez-vous sur https://iset.uvt.tn\n2. Allez dans la section Technologies Web\n3. Sélectionnez le module JavaScript\n\nLe cours fait partie du module Technologies Web : https://iset.uvt.tn/course/view.php?id=104"
                ]
            },
            {
                "patterns": [
                    "uvt", "plateforme uvt", "cours en ligne", "elearning",
                    "cours à distance", "formation en ligne"
                ],
                "responses": [
                    "La plateforme UVT-ISET (https://iset.uvt.tn/) propose plusieurs types de ressources en ligne :\n\n1. Auto-Formation :\n- Cours en auto-formation avec exercices et évaluations\n- Accès : https://iset.uvt.tn/course/index.php?categoryid=2\n\n2. Tutoriels :\n- Guides et tutoriels pratiques\n- Accès : https://iset.uvt.tn/course/index.php?categoryid=3\n\n3. Médiathèque :\n- Ressources multimédia pédagogiques\n- Accès : https://iset.uvt.tn/course/index.php?categoryid=4"
                ]
            },
            {
                "patterns": [
                    "cours java", "programmation java", "poo java", "java"
                ],
                "responses": [
                    "Le cours de Java est disponible sur la plateforme UVT :\n\nProgrammation Orientée Objet en Java :\n- Niveau : 2ème année\n- Format : Cours tuteuré\n- Contenu :\n  • Concepts de la POO\n  • Classes et Objets\n  • Héritage et Polymorphisme\n  • TPs appliqués\n\nAccès : https://iset.uvt.tn/course/view.php?id=102"
                ]
            },
            {
                "patterns": [
                    "cours php", "programmation php", "développement web php", "php"
                ],
                "responses": [
                    "Le cours de PHP fait partie du module Technologies Web :\n\nTechnologies Web (PHP/MySQL) :\n- Niveau : 2ème année\n- Format : Cours tuteuré\n- Contenu :\n  • HTML5 et CSS3\n  • JavaScript et DOM\n  • PHP et MySQL\n  • Projets Web\n\nAccès : https://iset.uvt.tn/course/view.php?id=104"
                ]
            },
            {
                "patterns": [
                    "cours programmation", "algorithmes", "algo"
                ],
                "responses": [
                    "Voici les cours de programmation disponibles :\n\n1. Algorithmes et Programmation Structurée (1ère année) :\n- Format : Auto-formation\n- Contenu :\n  • Introduction à l'algorithmique\n  • Structures de contrôle\n  • Tableaux et fonctions\n  • Exercices pratiques\n\n2. Programmation Orientée Objet en Java (2ème année)\n3. Technologies Web (PHP/MySQL) (2ème année)\n\nTous ces cours sont accessibles sur la plateforme UVT : https://iset.uvt.tn/"
                ]
            },
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
            }
        ]
        
        try:
            if os.path.exists('data/training_data.json'):
                print("Chargement du fichier training_data.json...")
                with open('data/training_data.json', 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # Fusionner les données par défaut avec les données chargées
                    return default_data + loaded_data
            print("Fichier training_data.json non trouvé, utilisation des données par défaut")
            return default_data
        except Exception as e:
            print(f"Erreur lors du chargement des données d'entraînement: {e}")
            return default_data

    def _load_scraped_data(self) -> dict:
        """Charge les données scrapées"""
        try:
            if os.path.exists('data/scraping-data.json'):
                print("Chargement du fichier data/scraping-data.json...")
                with open('data/scraping-data.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            print("Fichier data/scraping-data.json non trouvé")
            return {}
        except Exception as e:
            print(f"Erreur lors du chargement des données scrapées: {e}")
            return {}

    def generate_response(self, query: str) -> str:
        """Génère une réponse en priorisant les données scrapées"""
        if not query:
            return "Veuillez poser une question."

        query = query.lower().strip()
        print(f"Question reçue: {query}")

        # Vérifier si les données scrapées sont chargées
        if not self.scraped_data:
            print("ERREUR: Données scrapées non chargées")
            self.scraped_data = self._load_scraped_data()
            if not self.scraped_data:
                print("ERREUR: Impossible de charger les données scrapées")
                return "Désolé, je ne peux pas accéder aux informations pour le moment."

        # Mots clés pour la recherche
        keywords = {
            'formation': ['formation', 'formations', 'étudier', 'cursus', 'programme'],
            'formation_continue': ['formation continue', 'formation à distance', 'formation en ligne'],
            'masteres': ['mastere', 'mastères', 'master', 'masters'],
            'licence': ['licence', 'formation initiale'],
            'partenaires': ['partenaire', 'partenariat', 'entreprise'],
            'stages': ['stage', 'pfe', 'stages'],
            'contact': ['contact', 'adresse', 'téléphone', 'email'],
            'certifications': ['certification', 'microsoft', 'formation certifiante']
        }

        # Identifier la catégorie de la question
        category = None
        for cat, words in keywords.items():
            if any(word in query for word in words):
                category = cat
                break

        # Si une catégorie est identifiée, utiliser la réponse structurée
        if category:
            response = self._get_structured_response(category, query)
            if response:
                return response

        # En dernier recours, chercher dans les données d'entraînement
        for item in self.training_data:
            for pattern in item['patterns']:
                if query in pattern.lower() or pattern.lower() in query:
                    return item['responses'][0]

        return "Je ne comprends pas votre demande. Pouvez-vous reformuler votre question en précisant si vous souhaitez des informations sur :\n- Les formations (licence, mastère)\n- La formation continue\n- Les certifications\n- Les stages\n- Les partenaires\n- Les contacts"

    def _get_structured_response(self, category: str, query: str) -> Optional[str]:
        """Génère une réponse structurée basée sur la catégorie"""
        if category == 'formation':
            response = "Voici les formations disponibles à l'ISET Sfax :\n\n"
            
            # Ajouter les informations sur la licence
            if 'formations' in self.scraped_data and 'licence' in self.scraped_data['formations']:
                licence = self.scraped_data['formations']['licence']
                response += f"1. 📚 {licence['nom']}\n"
                response += f"   - Type : {licence['type']}\n"
                response += f"   - Description : {licence['description']}\n\n"
            
            # Ajouter les informations sur les mastères
            if 'formations' in self.scraped_data and 'masteres' in self.scraped_data['formations']:
                response += "2. Mastères professionnels :\n"
                for mastere in self.scraped_data['formations']['masteres']:
                    response += f"   📚 {mastere['nom']}\n"
                    response += f"   - Type : {mastere['type']}\n"
                    response += f"   - Description : {mastere['description']}\n\n"
            
            return response
            
        elif category == 'formation_continue':
            if 'formation_continue' in self.scraped_data:
                fc = self.scraped_data['formation_continue']
                response = f"{fc['presentation']}\n\n"
                response += "Types de formations disponibles :\n"
                for type_name, details in fc['types_formation'].items():
                    response += f"\n{details['nom']} :\n"
                    response += f"- Type : {details['type']}\n"
                    response += f"- Durée : {details['duree']}\n"
                    if 'modalites' in details:
                        response += "- Modalités :\n"
                        for mod_type, mod_desc in details['modalites'].items():
                            response += f"  • {mod_type} : {mod_desc}\n"
                return response
        
        elif category == 'stages':
            if 'stages' in self.scraped_data:
                stages = self.scraped_data['stages']
                response = "Informations sur les stages :\n\n"
                for stage in stages['types']:
                    response += f"📌 {stage['nom']}\n"
                    response += f"- Durée : {stage['duree']}\n"
                    response += f"- Niveau : {stage['niveau']}\n"
                    response += f"- Période : {stage['periode']}\n"
                    response += "- Documents requis :\n"
                    for doc in stage['documents_requis']:
                        response += f"  • {doc}\n"
                    response += "\n"
                response += "\nProcédure de stage :\n"
                for etape in stages['procedure']['etapes']:
                    response += f"- {etape}\n"
                response += f"\nContact service des stages :\n"
                response += f"Email : {stages['procedure']['contacts']['service_stages']}\n"
                response += f"Tél : {stages['procedure']['contacts']['tel']}"
                return response

        elif category == 'masteres':
            if 'formations' in self.scraped_data and 'masteres' in self.scraped_data['formations']:
                masteres = self.scraped_data['formations']['masteres']
                response = "Voici les mastères disponibles à l'ISET Sfax :\n\n"
                for mastere in masteres:
                    response += f"📚 {mastere['nom']}\n"
                    response += f"Type : {mastere['type']}\n"
                    response += f"Durée : {mastere.get('duree', '2 ans')}\n"
                    response += f"Description : {mastere['description']}\n"
                    if 'objectifs' in mastere:
                        response += "\nObjectifs :\n"
                        for obj in mastere['objectifs']:
                            response += f"- {obj}\n"
                    if 'debouches' in mastere:
                        response += "\nDébouchés :\n"
                        for deb in mastere['debouches']:
                            response += f"- {deb}\n"
                    response += "\n"
                return response

        elif category == 'licence':
            if 'formations' in self.scraped_data and 'licence' in self.scraped_data['formations']:
                licence = self.scraped_data['formations']['licence']
                response = f"📚 {licence['nom']}\n\n"
                response += f"Type : {licence['type']}\n"
                response += f"Description : {licence['description']}\n"
                response += f"Durée : {licence.get('duree', '3 ans')}\n\n"
                if 'specialites' in licence:
                    response += "Spécialités disponibles :\n"
                    for spec in licence['specialites']:
                        response += f"\n🔹 {spec['nom']}\n"
                        response += f"Description : {spec['description']}\n"
                        response += "Débouchés :\n"
                        for deb in spec['debouches']:
                            response += f"- {deb}\n"
                return response

        elif category == 'contact':
            if 'contact' in self.scraped_data:
                contact = self.scraped_data['contact']
                response = "📍 Coordonnées de l'ISET Sfax :\n\n"
                response += f"Adresse : {contact['adresse']}\n"
                response += f"Téléphone : {contact['tel']}\n"
                response += f"Fax : {contact['fax']}\n"
                response += f"Email : {contact['email']}\n"
                response += f"Horaires : {contact['horaires']}\n\n"
                if 'services' in contact:
                    response += "Services spécifiques :\n"
                    for service_name, service_info in contact['services'].items():
                        response += f"\n📌 Service {service_name} :\n"
                        response += f"- Email : {service_info['email']}\n"
                        response += f"- Tél : {service_info['tel']}\n"
                return response

        elif category == 'certifications':
            if 'formation_continue' in self.scraped_data and 'certifications' in self.scraped_data['formation_continue']:
                certif = self.scraped_data['formation_continue']['certifications']
                response = "🎓 Certifications disponibles :\n\n"
                for type_certif, details in certif.items():
                    response += f"📌 {details['nom']}\n"
                    if 'certifications_disponibles' in details:
                        for cert in details['certifications_disponibles']:
                            response += f"- {cert['nom']}\n"
                            response += f"  Durée : {cert['duree']}\n"
                            response += f"  Niveau : {cert['niveau']}\n"
                    elif 'programmes' in details:
                        for prog in details['programmes']:
                            response += f"- {prog['nom']}\n"
                            response += f"  Durée : {prog['duree']}\n"
                            if 'technologies' in prog:
                                response += f"  Technologies : {', '.join(prog['technologies'])}\n"
                    response += "\n"
                return response
        
        return None

    def load_responses(self):
        """Charge les réponses depuis le fichier responses.json"""
        try:
            with open('data/responses.json', 'r', encoding='utf-8') as f:
                self.responses = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des réponses: {e}")
            self.responses = {}

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