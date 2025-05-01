import nltk
import sys
import os

def setup_nltk():
    """Configure et télécharge les ressources NLTK nécessaires."""
    print("Configuration de NLTK...")
    
    # Définir le chemin de données NLTK
    nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
    if not os.path.exists(nltk_data_path):
        os.makedirs(nltk_data_path)
    
    # Liste des ressources nécessaires
    resources = [
        'punkt',
        'stopwords',
        'wordnet',
        'averaged_perceptron_tagger'
    ]
    
    # Télécharger chaque ressource
    for resource in resources:
        print(f"Téléchargement de {resource}...")
        try:
            nltk.download(resource, quiet=True)
            print(f"✓ {resource} installé avec succès")
        except Exception as e:
            print(f"✗ Erreur lors du téléchargement de {resource}: {str(e)}")
            sys.exit(1)
    
    print("\nConfiguration NLTK terminée avec succès!")

if __name__ == '__main__':
    setup_nltk() 