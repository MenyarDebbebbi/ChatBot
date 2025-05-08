from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.analysis import StemmingAnalyzer, LanguageAnalyzer
import os
import json

class SearchEngine:
    def __init__(self, index_dir="search_index"):
        """Initialise le moteur de recherche"""
        self.index_dir = index_dir
        self.analyzer = LanguageAnalyzer("fr")  # Analyseur pour le français
        
        # Définir le schéma de l'index
        self.schema = Schema(
            id=ID(stored=True),
            title=TEXT(analyzer=self.analyzer, stored=True),
            content=TEXT(analyzer=self.analyzer, stored=True),
            category=TEXT(stored=True),
            url=ID(stored=True)
        )
        
        # Créer ou ouvrir l'index
        if not os.path.exists(index_dir):
            os.makedirs(index_dir)
            self.ix = create_in(index_dir, self.schema)
        else:
            self.ix = open_dir(index_dir)

    def index_data(self, scraped_data):
        """Indexe les données scrapées"""
        writer = self.ix.writer()

        # Indexer les formations
        if 'formations' in scraped_data:
            # Indexer la licence
            if 'licence' in scraped_data['formations']:
                licence = scraped_data['formations']['licence']
                content = f"{licence['description']} {licence['type']}"
                if 'specialites' in licence:
                    for spec in licence['specialites']:
                        content += f" {spec['description']} {' '.join(spec['debouches'])}"
                
                writer.add_document(
                    id=f"licence",
                    title=licence['nom'],
                    content=content,
                    category="formation",
                    url="/formations/licence"
                )

            # Indexer les mastères
            if 'masteres' in scraped_data['formations']:
                for mastere in scraped_data['formations']['masteres']:
                    content = f"{mastere['description']} {mastere['type']}"
                    if 'objectifs' in mastere:
                        content += f" {' '.join(mastere['objectifs'])}"
                    if 'debouches' in mastere:
                        content += f" {' '.join(mastere['debouches'])}"
                    
                    writer.add_document(
                        id=f"mastere_{mastere['nom']}",
                        title=mastere['nom'],
                        content=content,
                        category="formation",
                        url="/formations/mastere"
                    )

        # Indexer la formation continue
        if 'formation_continue' in scraped_data:
            fc = scraped_data['formation_continue']
            for type_name, formation in fc['types_formation'].items():
                content = f"{formation['type']} {formation.get('description', '')}"
                if 'modalites' in formation:
                    content += f" {' '.join(str(val) for val in formation['modalites'].values())}"
                if 'programmes' in formation:
                    for prog in formation['programmes']:
                        content += f" {' '.join(prog['modules'])}"
                
                writer.add_document(
                    id=f"fc_{type_name}",
                    title=formation['nom'],
                    content=content,
                    category="formation_continue",
                    url="/formation-continue"
                )

        # Indexer les certifications
        if 'formation_continue' in scraped_data and 'certifications' in scraped_data['formation_continue']:
            certifs = scraped_data['formation_continue']['certifications']
            for type_certif, details in certifs.items():
                content = details['nom']
                if 'certifications_disponibles' in details:
                    for cert in details['certifications_disponibles']:
                        content += f" {cert['nom']} {cert['niveau']}"
                elif 'programmes' in details:
                    for prog in details['programmes']:
                        content += f" {prog['nom']} {' '.join(prog.get('technologies', []))}"
                
                writer.add_document(
                    id=f"certif_{type_certif}",
                    title=details['nom'],
                    content=content,
                    category="certification",
                    url="/certifications"
                )

        # Indexer les partenaires
        if 'partenaires_techniques' in scraped_data:
            for partenaire in scraped_data['partenaires_techniques']:
                content = f"{partenaire['type']} {partenaire['collaboration']}"
                writer.add_document(
                    id=f"partenaire_{partenaire['nom']}",
                    title=partenaire['nom'],
                    content=content,
                    category="partenaire",
                    url="/partenaires"
                )

        writer.commit()

    def search(self, query, limit=5):
        """Effectue une recherche dans l'index"""
        with self.ix.searcher() as searcher:
            # Recherche dans plusieurs champs
            parser = MultifieldParser(["title", "content"], self.schema)
            q = parser.parse(query)
            
            # Effectuer la recherche
            results = searcher.search(q, limit=limit)
            
            # Formater les résultats
            formatted_results = []
            for r in results:
                formatted_results.append({
                    'title': r['title'],
                    'category': r['category'],
                    'url': r['url'],
                    'score': r.score,
                    'highlights': r.highlights("content")
                })
            
            return formatted_results

    def format_search_results(self, results):
        """Formate les résultats de recherche en réponse lisible"""
        if not results:
            return "Aucun résultat trouvé. Veuillez reformuler votre question."

        response = "Voici les informations que j'ai trouvées :\n\n"
        
        for result in results:
            response += f"📌 {result['title']}\n"
            if result['highlights']:
                response += f"   {result['highlights']}\n"
            response += f"   ➜ Plus d'informations : {result['url']}\n\n"

        return response 