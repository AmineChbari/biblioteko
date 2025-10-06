## Violation de sécurité ou détection de connexion suspecte

**Description** :
Le système détecte des tentatives de connexion depuis des adresses IP ou des appareils inhabituels.

**Acteurs** :

* Utilisateur
* Système d’authentification
* Moniteur de sécurité
* Administrateur

**Préambule** :
Détecter les activités inhabituelles protège les comptes et l’intégrité du système.

**Étapes** :

1. L’utilisateur se connecte depuis une nouvelle adresse IP ou un autre pays.
2. Le système la signale comme suspecte.
3. Une vérification par e-mail ou un code 2FA est requise.
4. L’administrateur reçoit une alerte de sécurité.
5. Si l’activité est jugée malveillante, la session est terminée et le compte verrouillé.
