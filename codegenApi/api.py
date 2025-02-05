from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from langdetect import detect, DetectorFactory

# 🔹 Charger les variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Vérifier la clé API OpenAI
if not OPENAI_API_KEY:
    raise ValueError("⚠️ Clé API OpenAI manquante ! Ajoutez-la dans un fichier .env.")

# 🔹 Initialiser OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 🔹 Initialiser FastAPI
app = FastAPI(
    title="Code AI API",
    description="API pour génération, documentation, correction et complétion de code.",
    version="1.0.0"
)

# 🔹 Forcer la détection stable des langues
DetectorFactory.seed = 0

# 🔹 Modèle de requête
class CodeRequest(BaseModel):
    prompt: str

# ✅ Fonction générique pour appeler OpenAI avec gestion des erreurs
def call_openai_api(prompt, model="gpt-4-turbo", temperature=0.7, max_tokens=500):
    """ Appelle OpenAI et gère les erreurs correctement avec la nouvelle version. """
    try:
        print(f"📡 Envoi du prompt à OpenAI : {prompt}")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        print(f"✅ Réponse OpenAI reçue : {response.choices[0].message.content}")
        return response.choices[0].message.content.strip()
    
    except openai.APIError as e:  # ✅ Correction de `openai.error.OpenAIError`
        print(f"❌ Erreur OpenAI : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur OpenAI : {str(e)}")
    
    except Exception as e:
        print(f"❌ Erreur inconnue : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur inconnue : {str(e)}")

# ✅ Fonction pour détecter la langue du code
def detect_language(prompt):
    """ Détecte automatiquement la langue du code. """
    try:
        return detect(prompt)
    except:
        return "unknown"

# ✅ Endpoint pour la génération de code
@app.post("/generate")
def generate_code(request: CodeRequest):
    lang = detect_language(request.prompt)
    prompt = f"""
    🎯 Tu es un assistant expert en développement logiciel.
    ➡️ Génère du code **fonctionnel**, **modulaire**, et **optimisé** en {lang} basé sur la demande ci-dessous.

    🔹 **Instructions** :
    - Le code doit être **exécutable sans erreurs**.
    - Utilise des **bonnes pratiques** et un **style clair**.
    - Ajoute **des commentaires explicatifs** et un **exemple d'utilisation**.
    - Ne mets **aucun texte hors du code**.

    🔹 **Demande de l'utilisateur** :
    {request.prompt}

    📌 **Code généré** :
    """
    return {"code": call_openai_api(prompt)}

# ✅ Endpoint pour documenter un code
@app.post("/document")
def document_code(request: CodeRequest):
    lang = detect_language(request.prompt)
    prompt = f"""
    🎯 Tu es un expert en documentation de code.
    ➡️ **Ajoute uniquement des commentaires** clairs et concis pour expliquer chaque partie importante du code en {lang}.

    🔹 **Instructions** :
    - Ajoute des **commentaires courts et pertinents**.
    - Ne modifie **pas la structure du code**.
    - Ne génère **aucun texte hors du code**.

    🔹 **Code à documenter** :
    {request.prompt}

    📌 **Code avec documentation** :
    """

    return {"code": call_openai_api(prompt)}

# ✅ Endpoint pour corriger et optimiser un code
@app.post("/debug")
def debug_code(request: CodeRequest):
    lang = detect_language(request.prompt)
    prompt = f"""
    🎯 Tu es un expert en correction et optimisation de code.
    ➡️ Analyse le code en {lang}, **corrige les erreurs** et **optimise son efficacité**.

    🔹 **Instructions** :
    - Corrige les **bugs et erreurs de syntaxe**.
    - Améliore la **performance et la lisibilité**.
    - Ajoute **des commentaires expliquant les corrections**.
    - Ne change pas **inutilement la logique**.

    🔹 **Code à corriger** :
    {request.prompt}

    📌 **Code corrigé et optimisé** :
    """
    return {"code": call_openai_api(prompt)}

# ✅ Endpoint pour analyser et améliorer un code
@app.post("/review")
def review_code(request: CodeRequest):
    lang = detect_language(request.prompt)
    prompt = f"""
    🎯 Tu es un expert en relecture et analyse de code.
    ➡️ Analyse le code en {lang} et propose **des suggestions d'amélioration**.

    🔹 **Instructions** :
    - Identifie les **erreurs critiques** (logiques, syntaxiques, performances).
    - Détecte les **mauvaises pratiques** et suggère des corrections.
    - Vérifie la **sécurité et la maintenabilité**.
    - Fournis une **analyse claire et concise**.

    🔹 **Code à analyser** :
    {request.prompt}

    📌 **Analyse et suggestions** :
    """

    return {"review": call_openai_api(prompt)}

# ✅ Endpoint pour compléter un code partiel
@app.post("/complete")
def complete_code(request: CodeRequest):
    lang = detect_language(request.prompt)
    prompt = f"""
    🎯 Tu es un expert en complétion de code.
    ➡️ Complète le code en {lang} **de manière efficace et optimisée**.

    🔹 **Instructions** :
    - Respecte la **logique et le style** du code existant.
    - N’ajoute **que les éléments nécessaires**.
    - Optimise la **lisibilité et la performance**.

    🔹 **Code partiel** :
    {request.prompt}

    📌 **Code complété** :
    """
    return {"code": call_openai_api(prompt)}

# ✅ Endpoint pour l'auto-complétion utilisée par VS Code
@app.post("/autocomplete")
async def autocomplete(request: CodeRequest):
    """
    🔹 Endpoint pour générer du code basé sur un prompt.
    - Reçoit un `prompt` depuis VS Code.
    - Retourne un code généré par OpenAI.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Le prompt ne peut pas être vide.")
    lang = detect_language(request.prompt)
    prompt = f"""
    🎯 Tu es un assistant spécialisé en auto-complétion de code.
    ➡️ Complète la ligne suivante en {detect_language(request.prompt)} **avec UNE seule instruction**.

    🔹 **Instructions** :
    - **Complète uniquement la ligne actuelle**, ne génère pas plusieurs lignes.
    - **Ne commence pas une nouvelle ligne** après la suggestion.
    - **Ne génère pas un bloc entier de code**.
    - **Respecte la logique et le contexte du code donné**.
    - **Ne mets aucun texte explicatif ni balises Markdown (` ``` `).**
    - **La suggestion doit être courte, pertinente et utilisable immédiatement**.

    🔹 **Début du code** :
    {request.prompt}

    📌 **Suite suggérée (UNE seule ligne) :**
    """
    return {"code": call_openai_api(prompt)}

# ✅ Endpoint de test
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de génération et correction de code 🚀"}
