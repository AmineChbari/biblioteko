## Connexion administrateur et gestion des rôles

**Description** :
Un administrateur accède au panneau d’administration pour gérer les utilisateurs, les téléversements et les paramètres.

**Acteurs** :

* Administrateur
* Système d’authentification
* Module de contrôle d’accès

**Préambule** :
Les administrateurs disposent de privilèges élevés, nécessitant des mesures de sécurité renforcées (comme l’authentification à deux facteurs).

**Étapes** :

1. L’administrateur se connecte avec ses identifiants et son code 2FA.
2. Le contrôle d’accès vérifie le rôle et les permissions de l’administrateur.
3. Le panneau d’administration s’affiche avec les outils de modération.
4. Les actions (bannir un utilisateur, supprimer du contenu, etc.) sont consignées.
5. Le système conserve une piste d’audit pour la traçabilité.
