%% Basé sur le scénario [[upload_contenu_inapproprie.md]] avec un accent sur les droits d'auteur
classDiagram
    %% === Acteurs principaux ===
    class Utilisateur {
        -id : int
        -nom : string
        -email : string
        -statutCompte : string
        +televerserContenu(fichier)
        +recevoirNotification(message)
    }

    class Contenu {
        -id : int
        -titre : string
        -type : string
        -metadonnees : string
        -statut : string
        +analyser()
        +bloquer()
    }

    class SystemeFiltrage {
        -listeNoire : List~string~
        +analyserContenu(contenu : Contenu)
        +detecterContenuInapproprie(contenu : Contenu) : bool
        +ajouterBlacklist(titre : string)
    }

    class LLM_ProcesseurImages {
        +extraireTexte(image)
        +analyserSemantique(texte)
        +detecterCopyright(texte)
    }

    class Administrateur {
        -id : int
        -nom : string
        +examinerSignalement(signalement)
        +notifierUtilisateur(utilisateur : Utilisateur, message : string)
    }

    class Signalement {
        -id : int
        -type : string
        -gravite : string
        -rapport : string
        +genererRapport(contenu : Contenu)
    }

    %% === Relations entre classes ===
    Utilisateur --> Contenu : "téléverse"
    Contenu --> SystemeFiltrage : "analysé par"
    SystemeFiltrage --> LLM_ProcesseurImages : "utilise"
    SystemeFiltrage --> Signalement : "crée si contenu inapproprié"
    Signalement --> Administrateur : "notifie"
    Administrateur --> Utilisateur : "envoie avertissement/suspension"
    SystemeFiltrage --> Contenu : "bloque si illégal"
