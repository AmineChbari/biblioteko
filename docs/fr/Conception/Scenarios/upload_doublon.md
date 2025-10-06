## Téléversements en double du même livre

**Description** :
Plusieurs utilisateurs téléversent des scans de la même édition de livre, provoquant des doublons et de possibles conflits de droits d’auteur.

**Acteurs** :

* Plusieurs utilisateurs
* LLM / processeur de texte
* Indexeur de base de données
* Administrateur

**Préambule** :
Pour optimiser le stockage et éviter les doublons, le système doit identifier les livres identiques ou quasi identiques.

**Étapes** :

1. L’utilisateur téléverse un scan.
2. Le LLM extrait les métadonnées (titre, auteur, ISBN, éditeur, édition).
3. Le système compare les métadonnées et le texte avec les entrées existantes.
4. Si un doublon est trouvé, le téléversement est arrêté.
5. L’utilisateur est informé que le livre existe déjà dans la base de données.
6. L’administrateur reçoit un rapport récapitulatif des doublons.
