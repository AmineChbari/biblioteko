# Mise en place des scénarios

Ajout de 20 scénarios liés à l'utilisation de l'application par un utilisateur ou un administrateur.

# Mise en place de la CLI export_md

Ajout de la CLI pour exporter :
- Nom de fichier obligatoire, supporte les images et les pdf
- Options pour choisir le modèle à utiliser (gemini/mistral)
- Options pour limiter le nombre de pages à traiter

Exporte les documents dans `data/scans`.

### IMPORTANT :

L'export se fait via un chemin relatif `../..` pour trouver la racine du projet puis `data/scans`. C'est possiblement un point sensible à surveiller selon l'endroit où on lance le script.