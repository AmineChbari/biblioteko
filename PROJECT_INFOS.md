# 📘 PROJECT_INFOS

## 🧠 Présentation du projet

Ce projet a pour objectif de **numériser et d’extraire automatiquement le contenu de livres physiques** à l’aide de **reconnaissance d’image (OCR)** et de **modèles de langage avancés (LLM)** tels que **Gemini** et **Mistral**.
Le texte extrait est ensuite **converti et exporté au format Markdown (.md)** afin de faciliter l’édition, l’archivage ou l’analyse du contenu.

---

## 🗂️ Structure du projet (fichiers qui ont été modifiés/ajoutés)

```
project_root/
│
├── data/
│   ├── scans/               # Contient les fichiers exportés au format Markdown (.md)
│   └── temp/                # Contient les fichiers bruts issus de l’OCR (non versionnés)
│
├── src/
│   └── cli/
│       ├── OCR.py           # Script principal pour le traitement OCR et la reconnaissance d’image
│       └── export_md.py     # Module responsable de la génération et de l’export Markdown
│
├── .env.example             # Exemple de configuration des clés API et modèles
├── .gitignore               # Ignore data/temp, .venv, etc.
├── pyproject.toml           # Configuration Poetry + dépendances
├── README.md                # Présentation générale du projet
└── PROJECT_INFOS.md         # (ce fichier) — détails techniques et installation
```

> 💡 Le dossier `data/temp/` est ignoré par Git pour éviter d’ajouter les fichiers bruts lourds et temporaires produits par le pipeline d’OCR.

---

## ⚙️ Installation

### 1. Prérequis

* **Python 3.11+**
* **Poetry** installé globalement :

  ```bash
  pip install poetry
  ```
* (Optionnel mais recommandé) : **Virtualenv** activé automatiquement par Poetry.

---

### 2. Cloner le dépôt

```bash
git clone https://github.com/AmineChbari/biblioteko.git
cd <votre-projet>
```

---

### 3. Installer les dépendances

```bash
poetry install
```

Cela crée un environnement virtuel et installe toutes les dépendances définies dans `pyproject.toml` :

* **Flask** : pour l’interface web et les endpoints API
* **google-generativeai** : accès au modèle **Gemini**
* **mistralai** : intégration du modèle **Mistral**
* **pymupdf / fitz / pillow** : gestion et lecture d’images ou PDF
* **dotenv** : gestion de la configuration locale
* **pytest** : pour les tests unitaires

---

### 4. Configurer les variables d’environnement

Copiez le fichier `.env.example` en `.env` :

```bash
cp .env.example .env
```

Remplissez les clés d’API et modèles correspondants :

```bash
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-1.5-pro

MISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
MISTRAL_MODEL=mistral-large-latest
```

> 🔒 Les clés doivent provenir de vos comptes développeur Google (pour Gemini) et Mistral.ai.

---

[WIP]
## 🚀 Lancer l’application

### Exécution en local (avec Poetry)

```bash
poetry run flask run
```

L’application se lancera par défaut sur :

```
http://127.0.0.1:5000
```

---

## 🧩 Fonctionnement général

1. **Scan ou importation des pages** → déposées dans `data/temp/`.
2. **OCR + traitement d’image** → texte brut extrait des scans.
3. **Analyse et nettoyage par LLM** :

   * **Gemini** et/ou **Mistral** interprètent le contenu.
   * Mise en forme et correction du texte.
4. **Export Markdown** → fichier final enregistré dans `data/scans/` via le module `export_md`.

Exemple de sortie :

```
data/scans/
├── livre_exemple_1.md
└── chapitre_2_intro.md
```

---

## 🧪 Tests

Pour exécuter la suite de tests unitaires :

```bash
poetry run pytest
```

---

## 🧰 Développement

### Ajouter une dépendance

```bash
poetry add <package>
```

### Ajouter une dépendance de développement

```bash
poetry add --group dev <package>
```

### Mettre à jour les dépendances

```bash
poetry update
```

---

## 📦 Export et intégration

Les fichiers `.md` générés peuvent ensuite être :

* intégrés dans un CMS,
* analysés via un moteur de recherche local,
* ou utilisés dans des outils de traitement de texte avancés.

---