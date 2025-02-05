import * as vscode from 'vscode';
import axios from 'axios';

// Définition de l'URL de l'API FastAPI (assure-toi qu'elle tourne en local ou sur un serveur)
const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * 🚀 Fonction principale d'activation de l'extension VS Code
 * Elle enregistre les fonctionnalités et les événements.
 */
export function activate(context: vscode.ExtensionContext) {

    console.log("✅ CodeGen Extension activée !");

    // Collection pour afficher les suggestions d'amélioration de code (comme un linter)
    const diagnosticCollection = vscode.languages.createDiagnosticCollection("codeReview");

    /**
     * 🔹 Auto-complétion en temps réel avec InlineCompletionProvider
     * - Se déclenche quand l'utilisateur écrit du code
     * - Envoie le contexte à l'API et propose une suggestion
     */
    const autocompleteProvider = vscode.languages.registerInlineCompletionItemProvider(
        { scheme: 'file' },
        {
            async provideInlineCompletionItems(document, position, context, token) {
                console.log("🔍 Auto-complétion déclenchée !");
    
                // Récupère le texte avant le curseur
                const textBeforeCursor = document.getText(new vscode.Range(new vscode.Position(0, 0), position));
                console.log("🔎 Texte avant le curseur :", textBeforeCursor);
    
                if (textBeforeCursor.length < 3) {
                    console.log("⚠️ Texte trop court pour déclencher la complétion.");
                    return;
                }
    
                try {
                    console.log("⏳ Envoi de la requête à l'API FastAPI...");
                    const response = await axios.post(`${API_BASE_URL}/autocomplete`, { prompt: textBeforeCursor });
    
                    console.log("✅ Réponse API reçue :", response.data);
                    const suggestion = response.data.code;
    
                    return [new vscode.InlineCompletionItem(suggestion, new vscode.Range(position, position))];
                } catch (error) {
                    console.error("❌ Erreur d'auto-complétion :", error);
                    return [];
                }
            }
        }
    );
    

    // Ajout du provider à la liste des abonnements (subscriptions)
    context.subscriptions.push(autocompleteProvider);
    console.log("✅ Auto-complétion enregistrée !");

    /**
     * 🔍 Relecture de code après chaque sauvegarde (onDidSaveTextDocument)
     * - Analyse le code et affiche des suggestions comme un linter
     */
    vscode.workspace.onDidSaveTextDocument(async (document) => {
        const text = document.getText();
        if (!text.trim()) return;

        console.log("🔍 Relecture de code automatique...");

        try {
            const response = await axios.post(`${API_BASE_URL}/review`, { prompt: text });
            const review = response.data.review;

            const diagnostics: vscode.Diagnostic[] = [];
            const lines = document.getText().split("\n");

            // Parcourt chaque ligne du fichier pour détecter des suggestions
            lines.forEach((line, index) => {
                if (review.includes(line.trim())) {
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(new vscode.Position(index, 0), new vscode.Position(index, line.length)),
                        "💡 Suggestion d'amélioration : " + review,
                        vscode.DiagnosticSeverity.Information
                    );
                    diagnostics.push(diagnostic);
                }
            });

            // Ajoute les diagnostics à l'éditeur
            diagnosticCollection.set(document.uri, diagnostics);
        } catch (error) {
            console.error("❌ Erreur relecture de code :", error);
        }
    });

    /**
     * 🖥️ WebView pour interface utilisateur
     * - Permet d'utiliser les fonctionnalités via un menu interactif
     */
    const openWebviewCommand = vscode.commands.registerCommand('codegen.openWebview', () => {
        const panel = vscode.window.createWebviewPanel(
            'codegenWebview',
            'CodeGen Assistant',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );

        panel.webview.html = getWebviewContent();

        panel.webview.onDidReceiveMessage(async (message) => {
            console.log("📩 Message reçu depuis WebView:", message);
            await callApi(message.command, message.text, panel);
        }, undefined, context.subscriptions);
    });

    context.subscriptions.push(openWebviewCommand);
}

/**
 * 📡 Fonction générique pour appeler l'API FastAPI
 */
async function callApi(endpoint: string, input: string, panel?: vscode.WebviewPanel): Promise<void> {
    try {
        const response = await axios.post(`${API_BASE_URL}/${endpoint}`, { prompt: input });
        const result = response.data.code || response.data.review;

        console.log(`✅ Réponse API (${endpoint}):`, result);
        panel?.webview.postMessage({ result });
    } catch (error: unknown) {
        let errorMessage = "Erreur inconnue";

        if (axios.isAxiosError(error)) {
            errorMessage = error.response?.data?.detail || error.message;
        } else if (error instanceof Error) {
            errorMessage = error.message;
        }

        console.error(`❌ Erreur API (${endpoint}):`, errorMessage);
        panel?.webview.postMessage({ result: `❌ Erreur API : ${errorMessage}` });
    }
}



/**
 * 🖥️ Interface HTML du WebView pour interagir avec l'utilisateur
 */
function getWebviewContent(): string {
    return `
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CodeGen Assistant</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-gray-200 flex items-center justify-center min-h-screen">
        <div class="max-w-lg w-full bg-gray-800 shadow-lg rounded-xl p-6">
            <h1 class="text-2xl font-bold text-center text-blue-400 mb-6">🚀 CodeGen Assistant</h1>

            <label class="block text-sm font-semibold mb-2">💡 Décrivez votre besoin :</label>
            <textarea id="input" placeholder="Exemple : Générer une fonction Python..."
                class="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-300 focus:ring-2 focus:ring-blue-400 outline-none mb-4"></textarea>

            <label class="block text-sm font-semibold mb-2">🔍 Sélectionnez une action :</label>
            <select id="actionSelect"
                class="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-300 focus:ring-2 focus:ring-blue-400 outline-none mb-4">
                <option value="generate">🛠 Générer du code</option>
                <option value="document">📜 Documenter le code</option>
                <option value="debug">🐛 Déboguer le code</option>
                <option value="autocomplete">⚡ Auto-complétion</option>
                <option value="review">🔍 Relecture de code</option>
            </select>

            <button id="executeButton"
                class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 rounded-lg transition-all">
                ✨ Exécuter
            </button>

            <div id="output"
                class="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg min-h-[150px] text-gray-300 overflow-auto text-sm mt-2">
                💡 Le résultat apparaîtra ici...
            </div>
        </div>

        <script>
            const vscode = acquireVsCodeApi();
            document.getElementById('executeButton').addEventListener('click', () => {
                const selectedAction = document.getElementById('actionSelect').value;
                const text = document.getElementById('input').value.trim();
                vscode.postMessage({ command: selectedAction, text });
            });
        </script>
    </body>
    </html>
    `;
}

/**
 * 🚪 Désactive l'extension proprement
 */
export function deactivate() {}
