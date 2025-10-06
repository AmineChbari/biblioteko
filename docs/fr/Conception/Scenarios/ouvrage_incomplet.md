## Téléversement de livre incomplet

**Description** :
Un utilisateur téléverse seulement une partie d’un livre ou certaines pages manquent.

**Acteurs** :

* Utilisateur
* LLM / processeur de texte
* Vérificateur d’intégrité du système
* Administrateur

**Préambule** :
Pour garantir des livres complets, le système doit détecter les séquences de pages manquantes.

**Étapes** :

1. L’utilisateur téléverse plusieurs images de pages.
2. Le système détecte les numéros de pages (ex. 1, 2, 3, 7).
3. Les pages manquantes sont automatiquement signalées.
4. L’utilisateur est notifié des pages manquantes.
5. Le téléversement reste incomplet jusqu’à correction.
6. L’administrateur reçoit une liste des téléversements incomplets à examiner.
