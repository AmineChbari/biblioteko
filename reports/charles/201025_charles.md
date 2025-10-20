# Pistes pour les droits

## Comment reconnaître une oeuvre copyrightée

- Usurpation d'identité des concurrents (se faire passer pour des concurrents pour brouiller les pistes)
- Utilisation de plusieurs API pour vérifier si le livre est copyrighté, si une seule flag le livre : on le blacklist/refuse
- Construction d'une blacklist selon les résultats du LLM (le LLM fait des recherches pour savoir si oui ou non le livre est copyright)
- Fusion entre blacklist avec plusieurs API et LLM (redondance)

## Comment gérer

- Interdiction formelle d'upload
- Si détecté comme copyrighté, demander une authentification par Franceconnect, CI ou autre (autorisation conditionelle)
- Seulement autoriser la mention du livre
- Sous-entendre l'existence de sites hébergeant l'oeuvre ou lister des liens annexes (hors du site) pour pouvoir télécharger/consulter les livres
  
# Diagramme UML

Mise en place d'un début de diagramme de classe en se basant sur le scénario où un utilisateur envoie du contenu inapproprié (particulièrement du contenu copyrighté)