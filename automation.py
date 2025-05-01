import subprocess
import os
import sys
import logging
from datetime import datetime
import codecs

# Assurer que stdout utilise UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Configuration du logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class AutomationTasks:
    @staticmethod
    def run_tests():
        """Exécute les tests unitaires avec couverture"""
        logging.info("Exécution des tests unitaires avec couverture...")
        try:
            result = subprocess.run(['python', 'run_tests.py'], 
                                 capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                logging.info("Tests réussis [OK]")
                logging.info("Le rapport de couverture est disponible dans le dossier 'coverage_report'")
                return True
            else:
                logging.error(f"Échec des tests [X]\n{result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution des tests: {str(e)}")
            return False

    @staticmethod
    def build_docker():
        """Construit l'image Docker"""
        logging.info("Construction de l'image Docker...")
        try:
            result = subprocess.run(['docker-compose', 'build'], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("Image Docker construite avec succès [OK]")
                return True
            else:
                logging.error(f"Échec de la construction Docker [X]\n{result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Erreur lors de la construction Docker: {str(e)}")
            return False

    @staticmethod
    def deploy():
        """Déploie l'application"""
        logging.info("Déploiement de l'application...")
        try:
            result = subprocess.run(['docker-compose', 'up', '-d'], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("Application déployée avec succès [OK]")
                return True
            else:
                logging.error(f"Échec du déploiement [X]\n{result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Erreur lors du déploiement: {str(e)}")
            return False

    @staticmethod
    def backup_data():
        """Sauvegarde les données"""
        logging.info("Sauvegarde des données...")
        try:
            backup_dir = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Sauvegarde des fichiers importants
            files_to_backup = [
                'data/responses.json',
                'data/training_data.json',
                'web/static/images/attestations'
            ]
            
            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        subprocess.run(['cp', '-r', file_path, backup_dir])
                    else:
                        subprocess.run(['cp', file_path, backup_dir])
            
            logging.info(f"Sauvegarde terminée dans {backup_dir} [OK]")
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde: {str(e)}")
            return False

    @staticmethod
    def cleanup():
        """Nettoie les ressources inutilisées"""
        logging.info("Nettoyage des ressources...")
        try:
            # Supprimer les conteneurs arrêtés
            subprocess.run(['docker-compose', 'down'], capture_output=True)
            # Nettoyer les images non utilisées
            subprocess.run(['docker', 'system', 'prune', '-f'], capture_output=True)
            
            logging.info("Nettoyage terminé [OK]")
            return True
        except Exception as e:
            logging.error(f"Erreur lors du nettoyage: {str(e)}")
            return False

def main():
    """Point d'entrée principal pour l'automatisation"""
    if len(sys.argv) < 2:
        print("Usage: python automation.py [test|build|deploy|backup|cleanup|all]")
        return

    task = sys.argv[1].lower()
    automation = AutomationTasks()

    if task == 'test':
        automation.run_tests()
    elif task == 'build':
        automation.build_docker()
    elif task == 'deploy':
        automation.deploy()
    elif task == 'backup':
        automation.backup_data()
    elif task == 'cleanup':
        automation.cleanup()
    elif task == 'all':
        if automation.run_tests():
            if automation.build_docker():
                if automation.deploy():
                    automation.backup_data()

if __name__ == '__main__':
    main() 