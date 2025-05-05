#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction pour afficher les messages
print_message() {
    echo -e "${2}${1}${NC}"
}

# Vérifier si Docker est installé et en cours d'exécution
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_message "Docker n'est pas installé. Veuillez l'installer d'abord." "$RED"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_message "Le service Docker n'est pas en cours d'exécution." "$RED"
        exit 1
    fi
}

# Fonction pour construire les images
build() {
    print_message "Construction des images Docker..." "$YELLOW"
    docker-compose build --no-cache
}

# Fonction pour démarrer les conteneurs
start() {
    print_message "Démarrage des conteneurs..." "$YELLOW"
    docker-compose up -d
    print_message "Les conteneurs sont démarrés. L'application est accessible sur http://localhost" "$GREEN"
}

# Fonction pour arrêter les conteneurs
stop() {
    print_message "Arrêt des conteneurs..." "$YELLOW"
    docker-compose down
}

# Fonction pour afficher les logs
logs() {
    print_message "Affichage des logs..." "$YELLOW"
    docker-compose logs -f
}

# Fonction pour nettoyer
clean() {
    print_message "Nettoyage des ressources Docker..." "$YELLOW"
    docker-compose down -v
    docker system prune -f
}

# Vérifier Docker
check_docker

# Traiter les arguments
case "$1" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    logs)
        logs
        ;;
    clean)
        clean
        ;;
    *)
        echo "Usage: $0 {build|start|stop|restart|logs|clean}"
        exit 1
        ;;
esac 