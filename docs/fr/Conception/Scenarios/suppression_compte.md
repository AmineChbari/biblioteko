## Suppression de compte et effacement des données

**Description** :
Un utilisateur décide de supprimer son compte et toutes les données associées.

**Acteurs** :

* Utilisateur
* Système de base de données
* Administrateur

**Préambule** :
Conformément aux lois sur la protection des données (ex. RGPD), le système doit honorer les demandes de suppression de données personnelles.

**Étapes** :

1. L’utilisateur demande la suppression du compte via les paramètres.
2. Le système envoie un e-mail de confirmation.
3. Toutes les données personnelles et téléversements sont mises en file pour suppression.
4. L’administrateur est notifié pour validation finale.
5. Un journal de suppression est conservé à des fins de conformité.
