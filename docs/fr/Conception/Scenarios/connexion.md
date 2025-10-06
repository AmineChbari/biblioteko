## Connexion et gestion de session de l’utilisateur

**Description** :
Un utilisateur inscrit se connecte à son compte.

**Acteurs** :

* Utilisateur
* Système d’authentification
* Gestionnaire de session

**Préambule** :
Une connexion sécurisée et une bonne gestion des sessions préviennent les accès non autorisés et protègent les données des utilisateurs.

**Étapes** :

1. L’utilisateur saisit ses identifiants.
2. Le mot de passe est haché et comparé à celui stocké dans la base de données.
3. Si les informations sont correctes, le système crée une session sécurisée ou un jeton JWT.
4. L’utilisateur accède à son tableau de bord.
5. Les sessions inactives expirent automatiquement.
6. Plusieurs tentatives de connexion échouées entraînent un verrouillage temporaire du compte.
