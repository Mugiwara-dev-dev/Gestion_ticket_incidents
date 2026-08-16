from dao.incident_dao import IncidentDAO
from dao.intervention_dao import InterventionDAO
from dao.utilisateur_dao import UtilisateurDAO

class Interface:

    def afficher(self, utilisateur):


        if utilisateur["role"] == "Administrateur":
            self.menu_administrateur()

        elif utilisateur["role"] == "Technicien":
            self.menu_technicien()

        elif utilisateur["role"] == "Utilisateur":
            self.menu_utilisateur()

        else:
            print("Rôle inconnu.")

    def menu_administrateur(self):
        print()
        print("==========================================")
        print("          ESPACE ADMINISTRATEUR")
        print("==========================================")
        print("1. Ajouter un utilisateur")
        print("2. Liste des utilisateurs")
        print("3. Détails d'un utilisateur")
        print("4. Modifier un utilisateur")
        print("5. Supprimer un utilisateur")
        print("6. Rechercher un utilisateur")
        print("7. Consulter tous les incidents")
        print("8. Consulter les incidents ouverts")
        print("9. Consulter les incidents en cours")
        print("10. Ajouter une intervention")
        print("11. Résoudre un incident")
        print("12. Fermer un incident")
        print("13. Consulter mon historique")
        print("14. Statistiques et rapports")
        print("15. Se déconnecter")


    def menu_technicien(self):
        print()
        print("==========================================")
        print("          ESPACE TECHNICIEN")
        print("==========================================")
        print("1. Consulter les incidents ouverts")
        print("2. Consulter les incidents en cours")
        print("3. Prendre en charge un incident")
        print("4. Ajouter une intervention")
        print("5. Résoudre un incident")
        print("6. Fermer un incident")
        print("7. Consulter mon historique")
        print("8. Se déconnecter")


    def menu_utilisateur(self):
        print()
        print("==========================================")
        print("          ESPACE UTILISATEUR")
        print("==========================================")
        print("1. Créer un incident")
        print("2. Consulter mes incidents")
        print("3. Consulter le détail d'un incident")
        print("4. Filtrer mes incidents par statut")
        print("5. Filtrer mes incidents par priorité")
        print("6. Se déconnecter")

    def consulter_incidents(self):
        dao = IncidentDAO()
        incidents = dao.afficher_tous()
        print()
        print("========== LISTE DES INCIDENTS ==========")

        if not incidents:
            print("Aucun incident enregistré.")
            return

        for incident in incidents:
            print()
            print("ID :", incident["id_incident"])
            print("Titre :", incident["titre"])
            print("Description :", incident["description"])
            print("Date de création :", incident["date_creation"])
            print("Statut :", incident["statut"])
            print("Priorité :", incident["priorite"])
            print("ID utilisateur :", incident["id_utilisateur"])
            print("------------------------------------------")

    def signaler_incident(self, utilisateur):
        print()
        print("==========================================")
        print("           CRÉER UN INCIDENT")
        print("==========================================")

        titre = input("Titre : ")
        description = input("Description : ")
        print()
        print("Priorité :")
        print("1. FAIBLE")
        print("2. MOYENNE")
        print("3. HAUTE")
        choix = input("Choisissez la priorité : ")

        if choix == "1":
            priorite = "FAIBLE"

        elif choix == "2":
            priorite = "MOYENNE"

        elif choix == "3":
            priorite = "HAUTE"

        else:
            print("Priorité invalide.")
            return

        from models.incident import Incident
        from dao.incident_dao import IncidentDAO
        from datetime import datetime

        incident = Incident(
            None,
            titre,
            description,
            datetime.now(),
            "OUVERT",
            priorite,
            utilisateur["id_utilisateur"]
        )
        dao = IncidentDAO()
        dao.ajouter(incident)


    def consulter_mes_incidents(self, utilisateur):
        dao = IncidentDAO()
        incidents = dao.afficher_par_utilisateur(
            utilisateur["id_utilisateur"]
        )
        print()
        print("========== MES INCIDENTS ==========")

        if not incidents:
            print("Vous n'avez aucun incident enregistré.")
            return
        for incident in incidents:
            print()
            print("ID :", incident["id_incident"])
            print("Titre :", incident["titre"])
            print("Description :", incident["description"])
            print("Date de création :", incident["date_creation"])
            print("Statut :", incident["statut"])
            print("Priorité :", incident["priorite"])
            print("-----------------------------------")

    def choisir_incident(self):
        dao = IncidentDAO()
        incidents = dao.afficher_tous()
        print()
        print("========== INCIDENTS ==========")
        if not incidents:
            print("Aucun incident disponible.")
            return None
        for incident in incidents:
            print(
                incident["id_incident"],
                "-",
                incident["titre"],
                "| Statut :", incident["statut"],
                "| Priorité :", incident["priorite"]
            )
        print()
        try:
            id_incident = int(input("ID de l'incident : "))
        except ValueError:
            print("Veuillez saisir un numéro valide.")
            return None
        for incident in incidents:
            if incident["id_incident"] == id_incident:
                return incident
        print("Incident introuvable.")
        return None


    def consulter_interventions(self):
        from dao.intervention_dao import InterventionDAO

        dao = InterventionDAO()

        interventions = dao.afficher_toutes()

        print()
        print("========== LISTE DES INTERVENTIONS ==========")

        if not interventions:
            print("Aucune intervention enregistrée.")
            return

        for intervention in interventions:
            print()
            print("ID :", intervention["id_intervention"])
            print("Description :", intervention["description"])
            print("Date :", intervention["date_intervention"])
            print("Incident :", intervention["id_incident"])
            print("Technicien :", intervention["id_utilisateur"])
            print("----------------------------------------------")

    def consulter_detail_incident(self, utilisateur):
        print()
        print("==========================================")
        print("          DÉTAIL D'UN INCIDENT")
        print("==========================================")

        try:
            id_incident = int(
                input("ID de l'incident : ")
            )
        except ValueError:
            print("ID invalide.")
            return

        dao = IncidentDAO()

        incident = dao.afficher_par_id_et_utilisateur(
            id_incident,
            utilisateur["id_utilisateur"]
        )

        if incident is None:
            print()
            print("Incident introuvable ou accès refusé.")
            return

        print()
        print("--------------- INCIDENT ----------------")
        print("ID :", incident["id_incident"])
        print("Titre :", incident["titre"])
        print("Description :", incident["description"])
        print("Date :", incident["date_creation"])
        print("Priorité :", incident["priorite"])
        print("Statut :", incident["statut"])
        print("------------------------------------------")

        from dao.intervention_dao import InterventionDAO

        intervention_dao = InterventionDAO()

        interventions = intervention_dao.afficher_par_incident(
            id_incident
        )

        print()
        print("------------- INTERVENTIONS -------------")

        if not interventions:
            print("Aucune intervention pour cet incident.")
            return

        for intervention in interventions:
            print()
            print("ID intervention :", intervention["id_intervention"])
            print("Description :", intervention["description"])
            print("Date :", intervention["date_intervention"])
            print("Technicien :", intervention["id_utilisateur"])
            print("------------------------------------------")

    def filtrer_mes_incidents_statut(self, utilisateur):

        print()
        print("==========================================")
        print("      FILTRER MES INCIDENTS PAR STATUT")
        print("==========================================")
        print("1. OUVERT")
        print("2. EN_COURS")
        print("3. RESOLU")
        print("4. FERME")
        print("==========================================")

        choix = input("Choisissez un statut : ")

        if choix == "1":
            statut = "OUVERT"

        elif choix == "2":
            statut = "EN_COURS"

        elif choix == "3":
            statut = "RESOLU"

        elif choix == "4":
            statut = "FERME"

        else:
            print("Choix invalide.")
            return

        dao = IncidentDAO()

        incidents = dao.filtrer_par_statut(
            utilisateur["id_utilisateur"],
            statut
        )

        print()
        print("==========================================")
        print("       INCIDENTS :", statut)
        print("==========================================")

        if not incidents:
            print("Aucun incident avec ce statut.")
            return

        for incident in incidents:
            print()
            print("ID :", incident["id_incident"])
            print("Titre :", incident["titre"])
            print("Description :", incident["description"])
            print("Date :", incident["date_creation"])
            print("Priorité :", incident["priorite"])
            print("Statut :", incident["statut"])
            print("------------------------------------------")

    def filtrer_mes_incidents_priorite(self, utilisateur):

        print()
        print("==========================================")
        print("    FILTRER MES INCIDENTS PAR PRIORITÉ")
        print("==========================================")
        print("1. FAIBLE")
        print("2. MOYENNE")
        print("3. HAUTE")
        print("==========================================")

        choix = input("Choisissez une priorité : ")

        if choix == "1":
            priorite = "FAIBLE"

        elif choix == "2":
            priorite = "MOYENNE"

        elif choix == "3":
            priorite = "HAUTE"

        else:
            print("Choix invalide.")
            return

        dao = IncidentDAO()

        incidents = dao.filtrer_par_priorite(
            utilisateur["id_utilisateur"],
            priorite
        )

        print()
        print("==========================================")
        print("       INCIDENTS :", priorite)
        print("==========================================")

        if not incidents:
            print("Aucun incident avec cette priorité.")
            return

        for incident in incidents:
            print()
            print("ID :", incident["id_incident"])
            print("Titre :", incident["titre"])
            print("Description :", incident["description"])
            print("Date :", incident["date_creation"])
            print("Priorité :", incident["priorite"])
            print("Statut :", incident["statut"])


    def consulter_incidents_ouverts(self):

        dao = IncidentDAO()

        incidents = dao.afficher_par_statut("OUVERT")

        print()
        print("==========================================")
        print("       INCIDENTS OUVERTS")
        print("==========================================")

        if not incidents:
            print("Aucun incident ouvert.")
            return

        for incident in incidents:
            print()
            print("ID :", incident["id_incident"])
            print("Titre :", incident["titre"])
            print("Description :", incident["description"])
            print("Date :", incident["date_creation"])
            print("Priorité :", incident["priorite"])
            print("Statut :", incident["statut"])
            print(
                "Utilisateur :",
                incident["prenom"],
                incident["nom"]
            )


    def consulter_incidents_en_cours(self):
        dao = IncidentDAO()
        incidents = dao.afficher_par_statut("EN_COURS")
        print()
        print("==========================================")
        print("       INCIDENTS EN COURS")
        print("==========================================")
        if not incidents:
            print("Aucun incident en cours.")
            return
        for incident in incidents:
            print()
            print("ID :", incident["id_incident"])
            print("Titre :", incident["titre"])
            print("Description :", incident["description"])
            print("Date :", incident["date_creation"])
            print("Priorité :", incident["priorite"])
            print("Statut :", incident["statut"])
            print(
                "Utilisateur :",
                incident["prenom"],
                incident["nom"]
            )

    def prendre_en_charge_incident(self):
        print()
        print("==========================================")
        print("       PRENDRE EN CHARGE UN INCIDENT")
        print("==========================================")
        try:
            id_incident = int(
                input("ID de l'incident : ")
            )
        except ValueError:
            print("ID invalide.")
            return
        dao = IncidentDAO()
        dao.prendre_en_charge(id_incident)

    def ajouter_intervention(self, utilisateur):

        print()
        print("==========================================")
        print("          AJOUTER UNE INTERVENTION")
        print("==========================================")

        try:
            id_incident = int(
                input("ID de l'incident : ")
            )

            duree = int(
                input("Durée de l'intervention (minutes) : ")
            )

        except ValueError:
            print("Veuillez saisir des valeurs numériques valides.")
            return

        description = input("Commentaire : ")

        if not description.strip():
            print("Le commentaire ne peut pas être vide.")
            return

        if duree <= 0:
            print("La durée doit être supérieure à 0.")
            return

        dao = InterventionDAO()

        dao.ajouter_intervention(
            id_incident,
            utilisateur["id_utilisateur"],
            description,
            duree
        )

    def resoudre_incident(self):
        print()
        print("==========================================")
        print("          RÉSOUDRE UN INCIDENT")
        print("==========================================")
        try:
            id_incident = int(
                input("ID de l'incident : ")
            )
        except ValueError:
            print("ID invalide.")
            return

        dao = IncidentDAO()
        dao.resoudre_incident(id_incident)

    def fermer_incident(self):
        print()
        print("==========================================")
        print("          FERMER UN INCIDENT")
        print("==========================================")

        try:
            id_incident = int(
                input("ID de l'incident : ")
            )
        except ValueError:
            print("ID invalide.")
            return

        dao = IncidentDAO()
        dao.fermer_incident(id_incident)

    def consulter_historique(self, utilisateur):

        print()
        print("==========================================")
        print("          MON HISTORIQUE")
        print("==========================================")
        dao = IncidentDAO()
        incidents = dao.historique_technicien(
            utilisateur["id_utilisateur"]
        )
        if not incidents:
            print("Aucun incident traité.")
            return

        for incident in incidents:
            print()
            print("------------------------------------------")
            print("ID :", incident["id_incident"])
            print("Titre :", incident["titre"])
            print("Description :", incident["description"])
            print("Priorité :", incident["priorite"])
            print("Statut :", incident["statut"])
            print("------------------------------------------")

    def consulter_details_utilisateur(self):

        print()
        print("==========================================")
        print("       DÉTAILS D'UN UTILISATEUR")
        print("==========================================")

        try:
            id_utilisateur = int(input("ID de l'utilisateur : "))
        except ValueError:
            print("ID invalide.")
            return

        dao = UtilisateurDAO()

        utilisateur = dao.rechercher_par_id(id_utilisateur)

        if utilisateur is None:
            print("Utilisateur introuvable.")
            return

        print()
        print("------------------------------------------")
        print("ID :", utilisateur["id_utilisateur"])
        print("Nom :", utilisateur["nom"])
        print("Prénom :", utilisateur["prenom"])
        print("Login :", utilisateur["login"])
        print("Rôle :", utilisateur["role"])
        print("------------------------------------------")

    def modifier_utilisateur(self):
        print()
        print("==========================================")
        print("       MODIFIER UN UTILISATEUR")
        print("==========================================")

        try:
            id_utilisateur = int(
                input("ID de l'utilisateur : ")
            )
        except ValueError:
            print("ID invalide.")
            return

        dao = UtilisateurDAO()

        utilisateur = dao.rechercher_par_id(id_utilisateur)

        if utilisateur is None:
            print("Utilisateur introuvable.")
            return

        print()

        nom = input(
            f"Nom [{utilisateur['nom']}] : "
        )

        prenom = input(
            f"Prénom [{utilisateur['prenom']}] : "
        )

        login = input(
            f"Login [{utilisateur['login']}] : "
        )

        mot_de_passe = input(
            "Nouveau mot de passe : "
        )

        role = input(
            f"Rôle [{utilisateur['role']}] : "
        )

        if nom == "":
            nom = utilisateur["nom"]

        if prenom == "":
            prenom = utilisateur["prenom"]

        if login == "":
            login = utilisateur["login"]

        if mot_de_passe == "":
            mot_de_passe = utilisateur["mot_de_passe"]

        if role == "":
            role = utilisateur["role"]

        dao.modifier_utilisateur(
            id_utilisateur,
            nom,
            prenom,
            login,
            mot_de_passe,
            role
        )

    def supprimer_utilisateur(self):

        print()
        print("==========================================")
        print("       SUPPRIMER UN UTILISATEUR")
        print("==========================================")

        try:
            id_utilisateur = int(
                input("ID de l'utilisateur : ")
            )
        except ValueError:
            print("ID invalide.")
            return

        dao = UtilisateurDAO()

        utilisateur = dao.rechercher_par_id(id_utilisateur)

        if utilisateur is None:
            print("Utilisateur introuvable.")
            return

        print()
        print("Utilisateur :", utilisateur["nom"], utilisateur["prenom"])
        print("Login :", utilisateur["login"])

        confirmation = input(
            "Confirmer la suppression ? (O/N) : "
        )

        if confirmation.upper() != "O":
            print("Suppression annulée.")
            return

        dao.supprimer_utilisateur(id_utilisateur)

    def rechercher_utilisateur(self):

        print()
        print("==========================================")
        print("        RECHERCHER UN UTILISATEUR")
        print("==========================================")

        recherche = input(
            "Nom, prénom ou login : "
        )

        if recherche.strip() == "":
            print("Veuillez saisir une recherche.")
            return

        dao = UtilisateurDAO()

        utilisateurs = dao.rechercher_utilisateur(
            recherche
        )

        if not utilisateurs:
            print("Aucun utilisateur trouvé.")
            return

        print()
        print("==========================================")
        print("           RÉSULTATS")
        print("==========================================")

        for utilisateur in utilisateurs:
            print()
            print("------------------------------------------")
            print("ID :", utilisateur["id_utilisateur"])
            print("Nom :", utilisateur["nom"])
            print("Prénom :", utilisateur["prenom"])
            print("Login :", utilisateur["login"])
            print("Rôle :", utilisateur["role"])
            print("------------------------------------------")

    def ajouter_utilisateur(self):

        print()
        print("==========================================")
        print("          AJOUTER UN UTILISATEUR")
        print("==========================================")

        nom = input("Nom : ")
        prenom = input("Prénom : ")
        login = input("Login : ")
        mot_de_passe = input("Mot de passe : ")

        print()
        print("Choisir le rôle :")
        print("1. Utilisateur")
        print("2. Technicien")
        print("3. Administrateur")

        choix_role = input("Votre choix : ")

        if choix_role == "1":
            role = "Utilisateur"

        elif choix_role == "2":
            role = "Technicien"

        elif choix_role == "3":
            role = "Administrateur"

        else:
            print("Choix de rôle invalide.")
            return

        if not nom.strip() or not prenom.strip() or not login.strip() or not mot_de_passe.strip():
            print("Tous les champs sont obligatoires.")
            return

        dao = UtilisateurDAO()

        dao.ajouter_utilisateur(
            nom,
            prenom,
            login,
            mot_de_passe,
            role
        )

    def statistiques_rapports(self):

        print()
        print("==========================================")
        print("        STATISTIQUES ET RAPPORTS")
        print("==========================================")

        # Utilisateurs
        utilisateur_dao = UtilisateurDAO()
        nombre_utilisateurs = utilisateur_dao.nombre_utilisateurs()

        # Incidents
        incident_dao = IncidentDAO()
        total, par_statut, par_priorite = incident_dao.statistiques()

        # Interventions
        intervention_dao = InterventionDAO()
        nombre_interventions = intervention_dao.nombre_interventions()

        print()
        print("--------------- GÉNÉRAL -----------------")
        print("Nombre d'utilisateurs :", nombre_utilisateurs)
        print("Nombre total d'incidents :", total)
        print("Nombre d'interventions :", nombre_interventions)

        print()
        print("---------- INCIDENTS PAR STATUT ----------")

        if par_statut:
            for ligne in par_statut:
                print(
                    ligne["statut"],
                    ":",
                    ligne["nombre"]
                )
        else:
            print("Aucun incident.")

        print()
        print("--------- INCIDENTS PAR PRIORITÉ ---------")

        if par_priorite:
            for ligne in par_priorite:
                print(
                    ligne["priorite"],
                    ":",
                    ligne["nombre"]
                )
        else:
            print("Aucun incident.")

        print()
        print("==========================================")

    def consulter_utilisateurs(self):
        """Affiche la liste de tous les utilisateurs."""

        dao = UtilisateurDAO()

        utilisateurs = dao.get_all()

        print("\n==========================================")
        print("          LISTE DES UTILISATEURS")
        print("==========================================")

        if not utilisateurs:
            print("Aucun utilisateur trouvé.")
            return

        for utilisateur in utilisateurs:
            print("------------------------------------------")
            print("ID :", utilisateur["id_utilisateur"])
            print("Nom :", utilisateur["nom"])
            print("Prénom :", utilisateur["prenom"])
            print("Login :", utilisateur["login"])
            print("Rôle :", utilisateur["role"])

        print("------------------------------------------")
###############################################################################################
    def lancer(self, utilisateur):
        while True:
            self.afficher(utilisateur)
            choix = input("Votre choix : ")

            # ADMIN
            if utilisateur["role"] == "Administrateur":

                if choix == "1":
                    self.ajouter_utilisateur()

                elif choix == "2":
                    self.consulter_utilisateurs()

                elif choix == "3":
                    self.consulter_details_utilisateur()


                elif choix == "4":
                    self.modifier_utilisateur()


                elif choix == "5":
                    self.supprimer_utilisateur()


                elif choix == "6":
                    self.rechercher_utilisateur()

                elif choix == "7":
                    self.consulter_incidents()

                elif choix == "8":
                    self.consulter_incidents_ouverts()

                elif choix == "9":
                    self.consulter_incidents_en_cours()

                elif choix == "10":
                    self.ajouter_intervention(utilisateur)

                elif choix == "11":
                    self.resoudre_incident()

                elif choix == "12":
                    self.fermer_incident()

                elif choix == "13":
                    self.consulter_historique(utilisateur)


                elif choix == "14":
                    self.statistiques_rapports()

                elif choix == "15":
                    print("Déconnexion...")
                    break

                else:
                    print("Choix invalide.")

            # TECHNICIEN
            elif utilisateur["role"] == "Technicien":

                if choix == "1":
                    self.consulter_incidents_ouverts()

                elif choix == "2":
                    self.consulter_incidents_en_cours()

                elif choix == "3":
                    self.prendre_en_charge_incident()

                elif choix == "4":
                    self.ajouter_intervention(utilisateur)

                elif choix == "5":
                    self.resoudre_incident()

                elif choix == "6":
                    self.fermer_incident()

                elif choix == "7":
                    self.consulter_historique(utilisateur)

                elif choix == "8":
                    print("Déconnexion...")
                    break
                else:
                    print("Choix invalide.")

            # UTILISATEUR
            elif utilisateur["role"] == "Utilisateur":

                if choix == "1":
                    self.signaler_incident(utilisateur)

                elif choix == "2":
                    self.consulter_mes_incidents(utilisateur)

                elif choix == "3":
                    self.consulter_detail_incident(utilisateur)

                elif choix == "4":
                    self.filtrer_mes_incidents_statut(utilisateur)

                elif choix == "5":
                    self.filtrer_mes_incidents_priorite(utilisateur)

                elif choix == "6":
                    print("Déconnexion...")
                    break

                else:
                    print("Choix invalide.")