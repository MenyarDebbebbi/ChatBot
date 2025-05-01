# Utiliser une image Python officielle comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt setup_nltk.py ./

# Installer les dépendances et configurer NLTK
RUN pip install --no-cache-dir -r requirements.txt && \
    python setup_nltk.py

# Copier le reste du code source
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p web/static/images/attestations models/trained logs data

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE 5000

# Définir les variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Commande pour démarrer l'application
CMD ["flask", "run", "--host=0.0.0.0"] 