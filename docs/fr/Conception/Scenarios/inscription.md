## Inscription et vérification de l’utilisateur

**Description** :
Un nouvel utilisateur s’inscrit pour créer un compte afin de téléverser ou d’accéder à des livres.

**Acteurs** :

* Utilisateur
* Système d’authentification
* Service d’e-mail / de vérification
* Administrateur

**Préambule** :
La vérification des utilisateurs garantit la sécurité de la plateforme et empêche la création de comptes de spam ou de bots.

**Étapes** :

1. L’utilisateur remplit le formulaire d’inscription (nom d’utilisateur, e-mail, mot de passe).
2. Le système vérifie les doublons d’adresse e-mail ou de nom d’utilisateur.
3. Un e-mail ou SMS de vérification est envoyé.
4. L’utilisateur confirme via le lien de vérification.
5. Le compte est activé et enregistré dans la base de données des utilisateurs.
6. L’administrateur peut consulter les nouveaux comptes dans le tableau de bord.
