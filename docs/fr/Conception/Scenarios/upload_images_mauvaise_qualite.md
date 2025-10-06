## Image de mauvaise qualité ou scan illisible

**Description** :
Un utilisateur soumet une page de livre floue, de basse résolution ou partiellement capturée, qui ne peut pas être traitée correctement.

**Acteurs** :

* Utilisateur
* LLM / processeur d’images
* Système d’évaluation de la qualité
* Administrateur

**Préambule** :
Une image de mauvaise qualité peut entraîner des erreurs de transcription, un mauvais formatage ou des données incomplètes. Le système doit détecter ce problème et demander un nouveau téléversement.

**Étapes** :

1. L’utilisateur téléverse une image.
2. Le vérificateur de qualité évalue la netteté, l’éclairage et la couverture.
3. Si la qualité est en dessous du seuil, un avertissement est affiché.
4. L’utilisateur est invité à reprendre ou à retéléverser le scan.
5. Le système enregistre la tentative échouée.
6. Des soumissions répétées de mauvaise qualité déclenchent une révision par un administrateur.
