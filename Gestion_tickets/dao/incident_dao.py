from database.connexion import Connexion
from dao.base_dao import BaseDAO


class IncidentDAO(BaseDAO):

    def get_all(self):
        """Retourne tous les incidents."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            try:
                cursor = db.cursor(dictionary=True)

                sql = """
                SELECT *
                FROM incident
                ORDER BY id_incident
                """

                cursor.execute(sql)
                incidents = cursor.fetchall()

                cursor.close()

                return incidents

            except Exception as erreur:
                print(
                    "Erreur lors de la récupération des incidents :",
                    erreur
                )
                return []

        return []

    def get_by_id(self, id_element):
        """Retourne un incident à partir de son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            try:
                cursor = db.cursor(dictionary=True)

                sql = """
                SELECT *
                FROM incident
                WHERE id_incident = %s
                """

                cursor.execute(sql, (id_element,))
                incident = cursor.fetchone()

                cursor.close()

                return incident

            except Exception as erreur:
                print(
                    "Erreur lors de la recherche de l'incident :",
                    erreur
                )
                return None

        return None

    def delete_by_id(self, id_element):
        """Supprime un incident à partir de son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            try:
                cursor = db.cursor()

                sql = """
                DELETE FROM incident
                WHERE id_incident = %s
                """

                cursor.execute(sql, (id_element,))

                if cursor.rowcount > 0:
                    db.commit()
                    resultat = True
                else:
                    db.rollback()
                    resultat = False

                cursor.close()

                return resultat

            except Exception as erreur:
                db.rollback()

                print(
                    "Erreur lors de la suppression de l'incident :",
                    erreur
                )

                return False

        return False


    def ajouter(self, incident):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
            INSERT INTO incident
            (titre, description, date_creation, statut, priorite, id_utilisateur)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            valeurs = (
                incident.titre,
                incident.description,
                incident.date_creation,
                incident.statut,
                incident.priorite,
                incident.id_utilisateur
            )

            cursor.execute(sql, valeurs)
            db.commit()

            print("Incident ajouté avec succès !")

            cursor.close()
            db.close()

    def afficher_tous(self):
        connexion = Connexion()
        db = connexion.connecter()
        if db:
            cursor = db.cursor(dictionary=True)
            sql = """
            SELECT *
            FROM incident
            ORDER BY id_incident DESC
            """
            cursor.execute(sql)
            incidents = cursor.fetchall()
            cursor.close()
            db.close()
            return incidents
        return []

    def afficher_par_utilisateur(self, id_utilisateur):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM incident
            WHERE id_utilisateur = %s
            ORDER BY id_incident DESC
            """

            cursor.execute(sql, (id_utilisateur,))

            incidents = cursor.fetchall()

            cursor.close()
            db.close()

            return incidents
        return []

    def modifier_statut(self, id_incident, statut):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
            UPDATE incident
            SET statut = %s
            WHERE id_incident = %s
            """

            cursor.execute(sql, (statut, id_incident))
            db.commit()

            print("Statut de l'incident mis à jour !")

            cursor.close()
            db.close()

    def afficher_par_id(self, id_incident):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM incident
            WHERE id_incident = %s
            """

            cursor.execute(sql, (id_incident,))

            incident = cursor.fetchone()

            cursor.close()
            db.close()

            return incident
        return None

    def afficher_par_id_et_utilisateur(self, id_incident, id_utilisateur):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM incident
            WHERE id_incident = %s
            AND id_utilisateur = %s
            """

            cursor.execute(
                sql,
                (id_incident, id_utilisateur)
            )

            incident = cursor.fetchone()

            cursor.close()
            db.close()

            return incident
        return None

    def filtrer_par_statut(self, id_utilisateur, statut):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM incident
            WHERE id_utilisateur = %s
            AND statut = %s
            ORDER BY id_incident DESC
            """

            cursor.execute(
                sql,
                (id_utilisateur, statut)
            )

            incidents = cursor.fetchall()

            cursor.close()
            db.close()

            return incidents
        return []

    def filtrer_par_priorite(self, id_utilisateur, priorite):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM incident
            WHERE id_utilisateur = %s
            AND priorite = %s
            ORDER BY id_incident DESC
            """

            cursor.execute(
                sql,
                (id_utilisateur, priorite)
            )

            incidents = cursor.fetchall()

            cursor.close()
            db.close()

            return incidents
        return []

    def afficher_par_statut(self, statut):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT
                i.id_incident,
                i.titre,
                i.description,
                i.date_creation,
                i.statut,
                i.priorite,
                i.id_utilisateur,
                u.nom,
                u.prenom
            FROM incident i
            INNER JOIN utilisateur u
                ON i.id_utilisateur = u.id_utilisateur
            WHERE i.statut = %s
            ORDER BY i.id_incident DESC
            """

            cursor.execute(sql, (statut,))

            incidents = cursor.fetchall()

            cursor.close()
            db.close()

            return incidents
        return []

    def prendre_en_charge(self, id_incident):
        connexion = Connexion()
        db = connexion.connecter()
        if db:
            cursor = db.cursor()

            sql = """
            UPDATE incident
            SET statut = 'EN_COURS'
            WHERE id_incident = %s
            AND statut = 'OUVERT'
            """

            cursor.execute(sql, (id_incident,))

            if cursor.rowcount > 0:
                db.commit()
                print("Incident pris en charge avec succès !")
            else:
                print("Impossible de prendre en charge cet incident.")
                print("L'incident n'existe pas ou n'est pas OUVERT.")

            cursor.close()
            db.close()

    def resoudre_incident(self, id_incident):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
            UPDATE incident
            SET statut = 'RESOLU'
            WHERE id_incident = %s
            AND statut = 'EN_COURS'
            """

            cursor.execute(sql, (id_incident,))

            if cursor.rowcount > 0:
                db.commit()
                print("Incident résolu avec succès !")
            else:
                print("Impossible de résoudre cet incident.")
                print("L'incident n'existe pas ou n'est pas EN_COURS.")

            cursor.close()
            db.close()


    def fermer_incident(self, id_incident):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
               UPDATE incident
               SET statut = 'FERME'
               WHERE id_incident = %s
               AND statut = 'RESOLU'
               """

            cursor.execute(sql, (id_incident,))

            if cursor.rowcount > 0:
                db.commit()
                print("Incident fermé avec succès !")
            else:
                print("Impossible de fermer cet incident.")
                print("L'incident n'existe pas ou n'est pas RESOLU.")

            cursor.close()
            db.close()

    def historique_technicien(self, id_utilisateur):
        connexion = Connexion()
        db = connexion.connecter()
        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT DISTINCT
                i.id_incident,
                i.titre,
                i.description,
                i.priorite,
                i.statut
            FROM incident i
            INNER JOIN intervention inv
                ON i.id_incident = inv.id_incident
            WHERE inv.id_utilisateur = %s
            ORDER BY i.id_incident DESC
            """

            cursor.execute(sql, (id_utilisateur,))

            resultats = cursor.fetchall()

            cursor.close()
            db.close()

            return resultats
        return []

    def statistiques(self):

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            # Nombre total d'incidents
            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM incident
            """)
            total = cursor.fetchone()["total"]

            # Incidents par statut
            cursor.execute("""
                SELECT statut, COUNT(*) AS nombre
                FROM incident
                GROUP BY statut
            """)
            par_statut = cursor.fetchall()

            # Incidents par priorité
            cursor.execute("""
                SELECT priorite, COUNT(*) AS nombre
                FROM incident
                GROUP BY priorite
            """)
            par_priorite = cursor.fetchall()

            cursor.close()
            db.close()

            return total, par_statut, par_priorite
        return 0, [], []


    if __name__ == "__main__":
        dao = IncidentDAO()
        print("IncidentDAO fonctionne correctement.")