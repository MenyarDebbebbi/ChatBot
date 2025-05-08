import json
import csv
from datetime import datetime
import os

class ConversationHistory:
    def __init__(self, json_file='data/conversation_history.json', csv_file='data/conversation_history.csv'):
        """Initialise le gestionnaire d'historique des conversations"""
        self.json_file = json_file
        self.csv_file = csv_file
        self._ensure_files_exist()
        
    def _ensure_files_exist(self):
        """Assure que les fichiers d'historique existent"""
        os.makedirs('data', exist_ok=True)
        
        # Créer le fichier JSON s'il n'existe pas
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Créer le fichier CSV s'il n'existe pas
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'user_message', 'bot_response'])
    
    def add_conversation(self, user_message: str, bot_response: str):
        """Ajoute une conversation à l'historique"""
        timestamp = datetime.now().isoformat()
        
        # Ajouter au JSON
        try:
            with open(self.json_file, 'r+', encoding='utf-8') as f:
                conversations = json.load(f)
                conversations.append({
                    'timestamp': timestamp,
                    'user_message': user_message,
                    'bot_response': bot_response
                })
                f.seek(0)
                json.dump(conversations, f, ensure_ascii=False, indent=2)
                f.truncate()
        except Exception as e:
            print(f"Erreur lors de l'ajout à l'historique JSON: {e}")
        
        # Ajouter au CSV
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, user_message, bot_response])
        except Exception as e:
            print(f"Erreur lors de l'ajout à l'historique CSV: {e}")
    
    def get_history(self, format='json', limit=50):
        """Récupère l'historique des conversations"""
        if format == 'json':
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
                    return conversations[-limit:] if limit else conversations
            except Exception as e:
                print(f"Erreur lors de la lecture de l'historique JSON: {e}")
                return []
        
        elif format == 'csv':
            conversations = []
            try:
                with open(self.csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        conversations.append(row)
                    return conversations[-limit:] if limit else conversations
            except Exception as e:
                print(f"Erreur lors de la lecture de l'historique CSV: {e}")
                return []
    
    def clear_history(self):
        """Efface l'historique des conversations"""
        try:
            # Vider le fichier JSON
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            
            # Vider le fichier CSV
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'user_message', 'bot_response'])
            
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'historique: {e}")
            return False 