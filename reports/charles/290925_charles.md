# Qu'est-ce qui a été fait (résumé)

- Modification du .env
- Restructuration des notes (rapports)
- Ajout de certaines dépendances
- (WIP) Tuto pour installer et lancer le programme
- Utilisation de mistral et pixtral
- Tentative de détection du flou

# Modification du .env

Ajout des champs pour le modèle de gemini et clé + modèle de mistral

# Restructuration des notes

Ajout d'un dossier par étudiant avec un fichier commun pour les lier.

# Ajout de certaines dépendances

- Ajout de PyMuPDF + fitz pour la lecture de PDF
- Ajout de Google pour utiliser l'API google
- Ajout de MistralAI pour utiliser l'API de Mistral

# Utilisation de mistral et pixtral

J'ai tenté d'utiliser mistral et pixtral. \
De ce que j'ai observé, mistral (mistral-large-latest) a l'air de mieux gérer (moins d'erreurs) que pixtral (pixtral-large-latest) pour la reconnaissance de texte mais pixtral gère mieux la mise en page finale en markdown. \
Cependant, mistral gère moins bien la complétion de texte manquant que gemini. Par exemple, sur la page 2 de l'exemple "nettoyé", il n'arrive pas à compléter les nombres coupés et commence à 1 au lieu de 101.

# Tentative de détection du flou

Tentative d'utiliser un algorithme de variation de Laplace patch-par-patch sur une image pour détecter les endroits qui sont potentiellement flou. Fonctionne assez mal, retourne beaucoup de faux-positifs. \

Tentative de mise en place d'une vérification avec plusieurs algorithmes : Variance de Laplace, Edge detection et OCR avec tesseract. Fonctionne relativement bien sur des pages avec beaucoup de texte fin, mais sur des pages avec peu de texte ou avec une police d'écriture grande, cela retourne beaucoup de faux-positifs.