## Surcharge du serveur lors de téléversements massifs

**Description** :
Une montée soudaine des téléversements provoque des retards de traitement ou des plantages.

**Acteurs** :

* Plusieurs utilisateurs
* Gestionnaire de file d’attente
* Administrateur

**Préambule** :
Le système doit gérer les pics de charge sans perte de données ni incohérences de traitement.

**Étapes** :

1. De nombreux utilisateurs téléversent simultanément.
2. Le gestionnaire de file d’attente détecte l’augmentation de la charge.
3. Les téléversements sont mis en file et priorisés.
4. Les utilisateurs sont informés du délai estimé.
5. L’administrateur reçoit une alerte sur l’état du système.
6. Un mécanisme d’échelle automatique ou de limitation se déclenche.
