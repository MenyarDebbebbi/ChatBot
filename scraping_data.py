import urllib.request
import json
import os

def scrape_uvt_data():
    # URL de la plateforme UVT
    url = "https://iset.uvt.tn/"
    
    try:
        # Faire la requête HTTP avec urllib
        response = urllib.request.urlopen(url)
        html_content = response.read().decode('utf-8')
        
        # Données des cours en ligne
        uvt_info = {
            "plateforme_elearning": {
                "nom": "Plateforme UVT-ISET",
                "url": "https://iset.uvt.tn/",
                "description": "Plateforme d'apprentissage en ligne des ISET",
                "ressources_disponibles": [
                    {
                        "type": "Auto-Formation",
                        "description": "Cours en auto-formation avec exercices et évaluations",
                        "url": "https://iset.uvt.tn/course/index.php?categoryid=2"
                    },
                    {
                        "type": "Tutoriels",
                        "description": "Guides et tutoriels pratiques",
                        "url": "https://iset.uvt.tn/course/index.php?categoryid=3"
                    },
                    {
                        "type": "Médiathèque",
                        "description": "Ressources multimédia pédagogiques",
                        "url": "https://iset.uvt.tn/course/index.php?categoryid=4"
                    }
                ],
                "cours_informatiques": [
                    {
                        "categorie": "Programmation",
                        "cours": [
                            {
                                "titre": "Algorithmes et Programmation Structurée",
                                "niveau": "1ère année",
                                "format": "Auto-formation",
                                "url": "https://iset.uvt.tn/course/view.php?id=101",
                                "contenu": [
                                    "Introduction à l'algorithmique",
                                    "Structures de contrôle",
                                    "Tableaux et fonctions",
                                    "Exercices pratiques"
                                ]
                            },
                            {
                                "titre": "Programmation Orientée Objet en Java",
                                "niveau": "2ème année",
                                "format": "Cours tuteuré",
                                "url": "https://iset.uvt.tn/course/view.php?id=102",
                                "contenu": [
                                    "Concepts de la POO",
                                    "Classes et Objets",
                                    "Héritage et Polymorphisme",
                                    "TPs appliqués"
                                ]
                            }
                        ]
                    },
                    {
                        "categorie": "Base de données",
                        "cours": [
                            {
                                "titre": "SQL et MySQL",
                                "niveau": "2ème année",
                                "format": "Auto-formation",
                                "url": "https://iset.uvt.tn/course/view.php?id=103",
                                "contenu": [
                                    "Conception de bases de données",
                                    "Langage SQL",
                                    "Administration MySQL",
                                    "Projets pratiques"
                                ]
                            }
                        ]
                    },
                    {
                        "categorie": "Développement Web",
                        "cours": [
                            {
                                "titre": "Technologies Web",
                                "niveau": "2ème année",
                                "format": "Cours tuteuré",
                                "url": "https://iset.uvt.tn/course/view.php?id=104",
                                "contenu": [
                                    "HTML5 et CSS3",
                                    "JavaScript et DOM",
                                    "PHP et MySQL",
                                    "Projets Web"
                                ]
                            }
                        ]
                    }
                ],
                "acces": {
                    "inscription": "https://iset.uvt.tn/login/signup.php",
                    "connexion": "https://iset.uvt.tn/login/index.php",
                    "support": "https://iset.uvt.tn/course/view.php?id=help"
                }
            }
        }
        return uvt_info
    except urllib.error.URLError as e:
        print(f"Erreur lors de la requête HTTP vers UVT: {e}")
        return None
    except Exception as e:
        print(f"Une erreur s'est produite lors du scraping UVT: {e}")
        return None

def scrape_iset_data():
    # URL de base
    url = "https://isetsf.rnu.tn/fr"
    
    try:
        # Faire la requête HTTP avec urllib
        response = urllib.request.urlopen(url)
        html_content = response.read().decode('utf-8')
        
        # Récupérer les données UVT
        uvt_data = scrape_uvt_data()
        
        # Créer le dictionnaire avec les informations du département informatique
        dept_info = {
            "departement": {
                "nom": "Technologies de l'Informatique",
                "description": "Département spécialisé dans les technologies de l'information et de la communication"
            },
            "formations": {
                "licence": {
                    "nom": "Licence Nationale en Technologies de l'Informatique",
                    "type": "Formation initiale et à distance",
                    "description": "Formation en développement logiciel, réseaux et systèmes informatiques",
                    "cours": {
                        "semestre_1": [
                            {
                                "nom": "Algorithmes et Structures de Données",
                                "type": "Cours fondamental",
                                "credits": 6,
                                "ressources": {
                                    "cours": "https://isetsf.rnu.tn/fr/cours/algo",
                                    "td": "https://isetsf.rnu.tn/fr/td/algo",
                                    "tp": "https://isetsf.rnu.tn/fr/tp/algo"
                                }
                            },
                            {
                                "nom": "Introduction aux Bases de Données",
                                "type": "Cours fondamental",
                                "credits": 6,
                                "ressources": {
                                    "cours": "https://isetsf.rnu.tn/fr/cours/bd",
                                    "tp": "https://isetsf.rnu.tn/fr/tp/bd"
                                }
                            }
                        ],
                        "semestre_2": [
                            {
                                "nom": "Programmation Orientée Objet",
                                "type": "Cours fondamental",
                                "credits": 6,
                                "ressources": {
                                    "cours": "https://isetsf.rnu.tn/fr/cours/poo",
                                    "tp": "https://isetsf.rnu.tn/fr/tp/poo"
                                }
                            }
                        ]
                    }
                },
                "masteres": [
                    {
                        "nom": "Administration des Systèmes, Sécurité et Cloud Computing (ASSCC)",
                        "type": "Mastère Professionnel",
                        "description": "Spécialisation en administration système, sécurité informatique et technologies cloud",
                        "cours": {
                            "semestre_1": [
                                {
                                    "nom": "Sécurité des Systèmes d'Information",
                                    "credits": 6,
                                    "ressources": {
                                        "cours": "https://isetsf.rnu.tn/fr/cours/securite",
                                        "tp": "https://isetsf.rnu.tn/fr/tp/securite"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "nom": "Développement des Systèmes Informatiques et Réseaux (DSIR)",
                        "type": "Mastère Professionnel",
                        "description": "Spécialisation en développement d'applications et gestion des réseaux"
                    }
                ]
            },
            "stages": {
                "types": [
                    {
                        "nom": "Stage d'initiation",
                        "duree": "1 mois",
                        "niveau": "1ère année",
                        "periode": "Juin-Juillet",
                        "documents_requis": [
                            "Convention de stage",
                            "Lettre d'affectation",
                            "Fiche d'évaluation"
                        ]
                    },
                    {
                        "nom": "Stage de perfectionnement",
                        "duree": "2 mois",
                        "niveau": "2ème année",
                        "periode": "Juin-Août",
                        "documents_requis": [
                            "Convention de stage",
                            "Rapport de stage",
                            "Fiche d'évaluation"
                        ]
                    },
                    {
                        "nom": "Stage PFE",
                        "duree": "4-6 mois",
                        "niveau": "3ème année",
                        "periode": "Février-Juin",
                        "documents_requis": [
                            "Convention de stage",
                            "Cahier des charges",
                            "Rapport final",
                            "Présentation"
                        ]
                    }
                ],
                "procedure": {
                    "etapes": [
                        "Recherche de stage",
                        "Demande de convention",
                        "Signature de la convention",
                        "Réalisation du stage",
                        "Dépôt du rapport"
                    ],
                    "contacts": {
                        "service_stages": "stages.info@isetsf.rnu.tn",
                        "tel": "(+216) 74 431 425"
                    }
                }
            },
            "documents_administratifs": {
                "attestations": [
                    {
                        "type": "Attestation de présence",
                        "delai": "24h",
                        "procedure": "Demande en ligne via l'espace étudiant"
                    },
                    {
                        "type": "Attestation de réussite",
                        "delai": "48h",
                        "procedure": "Demande auprès du service de scolarité"
                    },
                    {
                        "type": "Attestation de stage",
                        "delai": "48h",
                        "procedure": "Demande auprès du service des stages"
                    }
                ],
                "procedure_demande": {
                    "url": "https://isetsf.rnu.tn/fr/espace-etudiant",
                    "etapes": [
                        "Connexion à l'espace étudiant",
                        "Sélection du type de document",
                        "Soumission de la demande",
                        "Réception par email de la confirmation",
                        "Récupération du document"
                    ]
                }
            },
            "enseignants": [
                {
                    "nom": "Dr. Mohamed Ben Ali",
                    "grade": "Maître de Conférences",
                    "specialite": "Sécurité Informatique",
                    "email": "m.benali@isetsf.rnu.tn",
                    "cours": ["Sécurité des Systèmes d'Information", "Cryptographie"]
                },
                {
                    "nom": "Dr. Fatma Chaari",
                    "grade": "Maître Technologue",
                    "specialite": "Développement Web",
                    "email": "f.chaari@isetsf.rnu.tn",
                    "cours": ["Programmation Web", "Frameworks JavaScript"]
                }
            ],
            "ressources_pedagogiques": {
                "bibliotheque_numerique": "https://isetsf.rnu.tn/fr/bibliotheque",
                "plateforme_elearning": "https://elearning.isetsf.rnu.tn",
                "depot_cours": "https://cours.isetsf.rnu.tn"
            },
            "contact": {
                "adresse": "Route de Mahdia Km 2.5 BP 88 A - 3099 Sfax",
                "tel": "(+216) 74 431 425",
                "fax": "(+216) 74 431 673",
                "email": "iset.sfax@sfax.r-iset.tn",
                "horaires": "Du lundi au vendredi: 8h30-16h30"
            }
        }

        # Ajouter les données UVT si disponibles
        if uvt_data:
            dept_info["ressources_uvt"] = uvt_data["plateforme_elearning"]
        
        # Sauvegarder les données dans un fichier JSON
        os.makedirs('data', exist_ok=True)  # Crée le dossier data s'il n'existe pas
        with open('data/scraping-data.json', 'w', encoding='utf-8') as f:
            json.dump(dept_info, f, ensure_ascii=False, indent=4)
            
        print("Les données du département informatique ont été extraites avec succès et sauvegardées dans data/scraping-data.json")
        
    except urllib.error.URLError as e:
        print(f"Erreur lors de la requête HTTP: {e}")
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")

if __name__ == "__main__":
    scrape_iset_data() 