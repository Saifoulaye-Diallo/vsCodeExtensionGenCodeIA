import os
import openai
import re
import sys
from dotenv import load_dotenv

# 🔹 Forcer l'encodage UTF-8 pour éviter les erreurs sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# 🔹 Charger la clé API OpenAI depuis .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Vérification de la clé API
if not OPENAI_API_KEY:
    raise ValueError("⚠️ Clé API OpenAI manquante ! Ajoutez-la dans un fichier .env.")

# 🔹 Initialisation du client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def call_openai_api(prompt):
    """ Appelle OpenAI pour générer du texte. """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur OpenAI : {str(e)}"

def detect_language(prompt):
    """ Détecte le langage du code à partir du prompt. """
    languages = ["Python", "Java", "C", "C++", "JavaScript", "TypeScript", "Go", "Rust", "PHP", "Swift", "Kotlin", "Ruby"]
    return next((lang for lang in languages if re.search(rf"\b{lang}\b", prompt, re.IGNORECASE)), "Python")

def generate_code(prompt):
    """ Génère uniquement du code avec des commentaires et un exemple d'utilisation. """
    full_prompt = f"""
    Tu es un assistant expert en programmation.
    Génère uniquement du code fonctionnel bien structuré avec des commentaires et un exemple d'utilisation.

    Instructions :
    - Génère du code avec des commentaires expliquant chaque partie importante.
    - Ajoute un exemple d'utilisation sous if __name__ == "__main__":.
    - Ne génère aucun texte explicatif en dehors du code.
    - Mets les commentaires et le code dans la langue saisie par l'utilisateur.

    Demande :
    {prompt}

    Code :
    """
    return call_openai_api(full_prompt)


def document_code(code):
    """ Ajoute des commentaires détaillés au code fourni. """
    full_prompt = f"""
    Tu es un expert en documentation de code.
    Ajoute des commentaires détaillés expliquant chaque ligne.
    Ne génère aucun texte explicatif en dehors du code.

    Code initial :
    {code}

    Code documenté :
    """
    return call_openai_api(full_prompt)

def debug_code(code):
    """ Débogue et optimise le code fourni. """   

    # Génère une correction sans explications hors du code
    full_prompt = f"""
    Tu es un expert en correction de code.
    Corrige les erreurs et optimise le code avec des commentaires clairs.

    Instructions :
    - Corrige uniquement les erreurs sans ajouter de texte hors du code.
    - Ajoute des commentaires expliquant chaque correction dans le code.
    - Ne génère pas d'introduction ni d'explications en dehors du code.

    Code à déboguer :
    {code}

    Code corrigé :
    """
    return call_openai_api(full_prompt)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Erreur : Utilisation : python generate.py <function> <input>")
        sys.exit(1)

    function_map = {
        "generate": generate_code,
        "document": document_code,
        "debug": debug_code
    }

    function = sys.argv[1]
    input_text = sys.argv[2]

    result = function_map.get(function, lambda x: "❌ Fonction non reconnue.")(input_text)
    print(result)
