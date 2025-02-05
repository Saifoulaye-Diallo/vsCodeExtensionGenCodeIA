# Utilisation de Node.js comme base
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN npm install

# Compiler l'extension avant l'exécution
RUN npm run compile

# Exposer le port (si nécessaire, pour debugging)
EXPOSE 3000

# Lancer l'extension en mode watch (dev)
CMD ["npm", "run", "watch"]
