## Mot de passe oublié / Récupération de compte

**Description** :
Un utilisateur ayant oublié son mot de passe demande à récupérer l’accès à son compte.

**Acteurs** :

* Utilisateur
* Système d’authentification
* Service d’e-mail

**Préambule** :
Une récupération de mot de passe sécurisée permet de restaurer l’accès sans compromettre la sécurité du compte.

**Étapes** :

1. L’utilisateur clique sur « Mot de passe oublié ».
2. Le système envoie un e-mail de récupération avec un lien à usage unique.
3. L’utilisateur définit un nouveau mot de passe conforme aux règles de sécurité.
4. Les anciennes sessions sont invalidées.
5. L’utilisateur se reconnecte avec succès.
6. L’administrateur peut consulter les journaux de récupération pour détecter une activité suspecte.
