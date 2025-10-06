## Mauvaise interprétation de la mise en page par le LLM

**Description** :
L’OCR ou le LLM interprète mal une mise en page complexe (ex. double colonne, notes de bas de page, illustrations).

**Acteurs** :

* Utilisateur
* LLM
* Analyseur de mise en page
* Administrateur

**Préambule** :
Pour garantir une représentation numérique fidèle, l’analyse de mise en page doit être robuste face aux structures complexes.

**Étapes** :

1. L’utilisateur téléverse une page à mise en page complexe.
2. Le LLM génère le texte mais perd la structure.
3. L’analyseur de mise en page détecte une divergence avec le format visuel.
4. Le système marque la page comme « à revoir ».
5. L’utilisateur ou l’administrateur corrige la mise en page manuellement.
