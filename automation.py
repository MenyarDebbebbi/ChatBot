import subprocess
import os
import sys
import logging
from datetime import datetime
import codecs
import shutil
import requests

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
    def __init__(self):
        self.required_dirs = ['logs', 'data', 'models/trained', 'web/static/images']
        self.setup_directories()

    def setup_directories(self):
        """Crée les répertoires nécessaires s'ils n'existent pas"""
        for directory in self.required_dirs:
            os.makedirs(directory, exist_ok=True)
            logging.info(f"Répertoire vérifié/créé: {directory}")

    def check_dependencies(self):
        """Vérifie les dépendances Python"""
        logging.info("Vérification des dépendances...")
        try:
            with open('requirements.txt', 'r') as f:
                requirements = f.read().splitlines()
            
            for req in requirements:
                try:
                    module = req.split('>=')[0]
                    __import__(module)
                    logging.info(f"✓ {module} est installé")
                except ImportError:
                    logging.error(f"✗ {module} n'est pas installé")
                    return False
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la vérification des dépendances: {str(e)}")
            return False

    def run_tests(self):
        """Exécute les tests unitaires avec couverture"""
        logging.info("Exécution des tests unitaires avec couverture...")
        try:
            # Nettoyer les fichiers de couverture précédents
            if os.path.exists('.coverage'):
                os.remove('.coverage')
            if os.path.exists('coverage_report'):
                shutil.rmtree('coverage_report')

            result = subprocess.run(['python', '-m', 'coverage', 'run', '-m', 'unittest', 'discover', 'tests'],
                                 capture_output=True, text=True)
            
            if result.returncode == 0:
                # Générer le rapport de couverture
                subprocess.run(['python', '-m', 'coverage', 'html', '--directory=coverage_report'])
                logging.info("Tests réussis [OK]")
                logging.info("Le rapport de couverture est disponible dans le dossier 'coverage_report'")
                return True
            else:
                logging.error(f"Échec des tests [X]\n{result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution des tests: {str(e)}")
            return False

    def check_docker_environment(self):
        """Vérifie si Docker est installé et fonctionnel"""
        try:
            result = subprocess.run(['docker', '--version'], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Docker est installé: {result.stdout.strip()}")
                return True
            else:
                logging.error("Docker n'est pas installé ou n'est pas accessible")
                return False
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de Docker: {str(e)}")
            return False

    def build_docker(self):
        """Construit l'image Docker"""
        if not self.check_docker_environment():
            return False

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

    def deploy(self):
        """Déploie l'application"""
        logging.info("Déploiement de l'application...")
        try:
            # Arrêter les conteneurs existants
            subprocess.run(['docker-compose', 'down'], capture_output=True)
            
            # Démarrer les nouveaux conteneurs
            result = subprocess.run(['docker-compose', 'up', '-d'], 
                                 capture_output=True, text=True)
            
            if result.returncode == 0:
                # Vérifier que l'application est accessible
                try:
                    response = requests.get('http://localhost:5000/health')
                    if response.status_code == 200:
                        logging.info("Application déployée et accessible [OK]")
                        return True
                except:
                    logging.warning("Application déployée mais potentiellement inaccessible")
                    return True
            else:
                logging.error(f"Échec du déploiement [X]\n{result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Erreur lors du déploiement: {str(e)}")
            return False

    def backup_data(self):
        """Sauvegarde les données"""
        logging.info("Sauvegarde des données...")
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = f"backups/backup_{timestamp}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Fichiers à sauvegarder
            files_to_backup = [
                'data/responses.json',
                'data/training_data.json',
                'web/static/images/attestations',
                'models/trained',
                'logs'
            ]
            
            for path in files_to_backup:
                if os.path.exists(path):
                    dst = os.path.join(backup_dir, os.path.basename(path))
                    if os.path.isdir(path):
                        shutil.copytree(path, dst)
                    else:
                        shutil.copy2(path, dst)
            
            # Créer une archive
            shutil.make_archive(backup_dir, 'zip', backup_dir)
            shutil.rmtree(backup_dir)  # Supprimer le dossier temporaire
            
            logging.info(f"Sauvegarde terminée: {backup_dir}.zip [OK]")
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde: {str(e)}")
            return False

    def cleanup(self):
        """Nettoie les ressources inutilisées"""
        logging.info("Nettoyage des ressources...")
        try:
            # Arrêter et supprimer les conteneurs
            subprocess.run(['docker-compose', 'down', '--remove-orphans'], 
                         capture_output=True)
            
            # Nettoyer les images non utilisées
            subprocess.run(['docker', 'system', 'prune', '-f'], 
                         capture_output=True)
            
            # Nettoyer les fichiers temporaires
            patterns = ['*.pyc', '*.pyo', '*.pyd', '__pycache__']
            for pattern in patterns:
                os.system(f'find . -name "{pattern}" -type f -delete')
            
            logging.info("Nettoyage terminé [OK]")
            return True
        except Exception as e:
            logging.error(f"Erreur lors du nettoyage: {str(e)}")
            return False

def main():
    """Point d'entrée principal pour l'automatisation"""
    if len(sys.argv) < 2:
        print("Usage: python automation.py [check|test|build|deploy|backup|cleanup|all]")
        return

    task = sys.argv[1].lower()
    automation = AutomationTasks()

    if task == 'check':
        automation.check_dependencies()
    elif task == 'test':
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
        success = True
        steps = [
            ('Vérification des dépendances', automation.check_dependencies),
            ('Tests unitaires', automation.run_tests),
            ('Construction Docker', automation.build_docker),
            ('Déploiement', automation.deploy),
            ('Sauvegarde', automation.backup_data)
        ]
        
        for step_name, step_func in steps:
            logging.info(f"\n=== {step_name} ===")
            if not step_func():
                success = False
                logging.error(f"Échec à l'étape: {step_name}")
                break
        
        if success:
            logging.info("\n✓ Toutes les étapes ont été complétées avec succès!")
        else:
            logging.error("\n✗ Le processus s'est arrêté en raison d'une erreur")

if __name__ == '__main__':
    main() 