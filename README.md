# 🚀 CodeGen Extension - VS Code

> **Extension VS Code pour la génération automatique de code via OpenAI 🚀**

## 📌 Description
CodeGen Extension est une **extension VS Code** qui utilise **OpenAI GPT-4** pour :
- Générer automatiquement du code basé sur un prompt.
- Compléter le code en ligne en temps réel.
- Relire et optimiser du code existant.
- Ajouter des commentaires pour documenter du code.
- Fournir une interface WebView intégrée pour interagir avec l’IA.

Le projet est **complètement dockerisé** avec **un frontend pour VS Code et un backend FastAPI**.

---

## ⚙️ Fonctionnalités
✅ **Génération de code** en fonction d'une description.  
✅ **Complétion automatique** en temps réel dans l’éditeur.  
✅ **Relecture et correction** avec suggestions d’amélioration.  
✅ **Documentation automatique** avec des commentaires clairs.  
✅ **Interface WebView** pour interaction utilisateur.  

---

## 📦 Installation et Configuration
### **1️⃣ Cloner le projet**
```sh
git clone https://github.com/Saifoulaye-Diallo/vsCodeExtensionGenCodeIA.git
cd vsCodeExtensionGenCodeIA
```

### **2️⃣ Configurer les variables d’environnement**
Dans `codegenApi/`, crée un fichier `.env` avec ta clé OpenAI :
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx
```

---

## 🐳 Exécution avec Docker
### **1️⃣ Construire et exécuter les conteneurs**
```sh
docker-compose up --build
```
📌 **L’extension et l’API seront lancées automatiquement**.

### **2️⃣ Vérifier si l’API fonctionne**
Dans un navigateur ou via `curl` :
```sh
curl http://127.0.0.1:8000/
```
✅ **Réponse attendue :**
```json
{"message":"Bienvenue sur l'API de génération et correction de code 🚀"}
```

---

## 🖥️ Lancer l’extension VS Code en mode développement
### **1️⃣ Ouvrir l'extension dans VS Code**
```sh
code .
```

### **2️⃣ Lancer l’extension en mode Dev**
Dans **VS Code**, exécute :  
🔹 **Ouvrir la palette de commandes (`Ctrl + Shift + P`)**  
🔹 **Sélectionner `Run Extension`**

---

## 📜 API Endpoints (FastAPI)
| **Méthode**| **Endpoint**    | **Description**                 |
|------------|-----------------|---------------------------------|
| `POST`     | `/generate`     | Génération de code              |
| `POST`     | `/autocomplete` | Complétion automatique          |
| `POST`     | `/review`       | Relecture et suggestions        |
| `POST`     | `/debug`        | Correction et optimisation      |
| `POST`     | `/document`     | Documentation du code           |
| `GET`      | `/`             | Vérification du statut de l’API |

---

## 📜 Structure du projet
📂 `codegen/` → **Frontend de l’extension (VS Code)**  
📂 `codegenApi/` → **Backend FastAPI pour OpenAI**  
📜 `Dockerfile` → **Configuration Docker pour le backend**  
📜 `docker-compose.yml` → **Orchestration des services**  
📜 `README.md` → **Documentation du projet**  

---

## 🔧 Développement et Débogage
### **Vérifier les logs des conteneurs**
```sh
docker-compose logs -f
```

### **Arrêter les conteneurs**
```sh
docker-compose down
```

### **Recompiler le code TypeScript**
```sh
npm run compile
```

---

## 📌 Contributions
1️⃣ **Fork** le projet  
2️⃣ **Crée une branche (`feature/new-feature`)**  
3️⃣ **Ajoute tes modifications**  
4️⃣ **Fais une pull request**  

✅ Toute contribution est la bienvenue ! 🚀

---

## ⚡ Auteur
👤 **Saifoulaye Diallo**  
📌 **Projet développé dans le cadre de l'UQAR - Hiver 2025**  

🌍 **Github** : [@Saifoulaye-Diallo](https://github.com/Saifoulaye-Diallo)  

---

🚀 **Merci d’utiliser CodeGen Extension !** 🎉

