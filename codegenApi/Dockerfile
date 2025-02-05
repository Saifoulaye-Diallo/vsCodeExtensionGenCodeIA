# Utilisation de Python 3.10 comme base
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . .
COPY .env .env
# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'API FastAPI
EXPOSE 8000

# Démarrer FastAPI avec Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
