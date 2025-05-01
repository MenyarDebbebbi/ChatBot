import unittest
import coverage
import sys
import os

def run_tests_with_coverage():
    # Démarrer la couverture
    cov = coverage.Coverage(
        source=['models', 'web'],
        omit=['*/__init__.py', '*/tests/*', '*/venv/*']
    )
    cov.start()

    # Découvrir et exécuter les tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Configurer le runner avec verbosité
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Arrêter la couverture et générer le rapport
    cov.stop()
    cov.save()
    
    # Créer le répertoire pour les rapports s'il n'existe pas
    os.makedirs('coverage_report', exist_ok=True)
    
    # Générer les rapports
    cov.html_report(directory='coverage_report')
    print("\nRapport de couverture généré dans le dossier 'coverage_report'")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1) 