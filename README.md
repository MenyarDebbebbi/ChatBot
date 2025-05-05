# Chatbot ISET Sfax 🤖

Un chatbot intelligent pour l'Institut Supérieur des Études Technologiques de Sfax, conçu pour répondre aux questions des étudiants et fournir des informations sur l'institut.

## 🌟 Fonctionnalités

- 💬 Interface de chat interactive
- 🎯 Réponses contextuelles intelligentes
- 🗣️ Support de la reconnaissance vocale
- 📄 Génération d'attestations automatique
- 🌙 Mode sombre/clair
- 🌐 Support multilingue (Français/Arabe)
- 📱 Interface responsive

## 🛠️ Technologies Utilisées

- **Backend** :

  - Python 3.9
  - Flask
  - NLTK
  - scikit-learn
  - Gunicorn

- **Frontend** :

  - HTML5/CSS3
  - JavaScript
  - Font Awesome
  - Web Speech API

- **Infrastructure** :
  - Docker
  - Nginx
  - Docker Compose

## 📋 Prérequis

- Docker et Docker Compose
- Git
- Python 3.9+ (pour le développement local)

## 🚀 Installation

1. **Cloner le repository**

   ```bash
   git clone https://github.com/votre-repo/iset-chatbot.git
   cd iset-chatbot
   ```

2. **Configuration**

   ```bash
   # Rendre le script de gestion Docker exécutable
   chmod +x docker-manage.sh
   ```

3. **Construction et démarrage**

   ```bash
   # Construire les images Docker
   ./docker-manage.sh build

   # Démarrer les conteneurs
   ./docker-manage.sh start
   ```

## 🎮 Utilisation

Une fois démarré, le chatbot est accessible à :

- Interface web : http://localhost
- API directe : http://localhost:5000

### Commandes Docker disponibles

```bash
# Voir les logs
./docker-manage.sh logs

# Redémarrer les services
./docker-manage.sh restart

# Arrêter les services
./docker-manage.sh stop

# Nettoyer les ressources
./docker-manage.sh clean
```

## 🏗️ Architecture

```
iset-chatbot/
├── app.py                 # Point d'entrée de l'application
├── models/               # Modèles NLP et logique métier
├── web/                  # Interface utilisateur
│   ├── static/          # Ressources statiques
│   └── templates/       # Templates HTML
├── data/                # Données d'entraînement et réponses
├── tests/               # Tests unitaires et d'intégration
└── docker/              # Configuration Docker
```

## 🔧 Configuration

### Variables d'environnement

```env
FLASK_APP=app.py
FLASK_ENV=production
PYTHONIOENCODING=utf-8
TZ=Africa/Tunis
```

### Configuration Nginx

Le fichier `nginx.conf` contient la configuration du serveur web, incluant :

- Gestion des fichiers statiques
- Proxy inverse vers l'application Flask
- Configuration SSL (si activée)
- Gestion des timeouts

## 📊 Tests

```bash
# Exécuter les tests unitaires
python -m unittest discover tests

# Exécuter les tests avec couverture
python -m coverage run -m unittest discover tests
python -m coverage report
```

## 🔍 Monitoring

- **Healthcheck** : http://localhost/health
- **Logs** : Disponibles via `./docker-manage.sh logs`
- **Métriques** : Accessibles via l'interface de monitoring Docker

## 🔐 Sécurité

- Données sensibles stockées dans des volumes Docker
- Accès en lecture seule aux données dans les conteneurs
- Proxy inverse Nginx pour la sécurité
- Limitation des ressources Docker
- Healthchecks pour la stabilité

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- ISET Sfax Team
- Contributeurs

## 📞 Support

Pour toute question ou problème :

- Ouvrir une issue sur GitHub
- Contacter l'équipe de support : support@isetsfax.tn
