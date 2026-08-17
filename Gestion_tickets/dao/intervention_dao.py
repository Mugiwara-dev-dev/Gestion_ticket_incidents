from database.connexion import Connexion
from dao.base_dao import BaseDAO

class InterventionDAO(BaseDAO):

    def get_all(self):
        """Retourne toutes les interventions."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            try:
                cursor = db.cursor(dictionary=True)

                sql = """
                SELECT *
                FROM intervention
                ORDER BY id_intervention
                """

                cursor.execute(sql)
                interventions = cursor.fetchall()

                cursor.close()

                return interventions

            except Exception as erreur:
                print(
                    "Erreur lors de la récupération des interventions :",
                    erreur
                )
                return []

        return []

    def get_by_id(self, id_element):
        """Retourne une intervention par son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            try:
                cursor = db.cursor(dictionary=True)

                sql = """
                SELECT *
                FROM intervention
                WHERE id_intervention = %s
                """

                cursor.execute(sql, (id_element,))
                intervention = cursor.fetchone()

                cursor.close()

                return intervention

            except Exception as erreur:
                print(
                    "Erreur lors de la recherche de l'intervention :",
                    erreur
                )
                return None

        return None

    def delete_by_id(self, id_element):
        """Supprime une intervention par son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            try:
                cursor = db.cursor()

                sql = """
                DELETE FROM intervention
                WHERE id_intervention = %s
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
                    "Erreur lors de la suppression de l'intervention :",
                    erreur
                )

                return False

        return False
    def get_all(self):
        """Retourne tous les utilisateurs."""

        connexion = Connexion()
        db = connexion.connecter()

        try:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM utilisateur
            ORDER BY id_utilisateur
            """

            cursor.execute(sql)
            utilisateurs = cursor.fetchall()

            cursor.close()

            return utilisateurs

        except Exception as erreur:
            print("Erreur lors de la récupération des utilisateurs :", erreur)
            return []

    def get_by_id(self, id_element):
        """Retourne un utilisateur par son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        try:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM utilisateur
            WHERE id_utilisateur = %s
            """

            cursor.execute(sql, (id_element,))
            utilisateur = cursor.fetchone()

            cursor.close()

            return utilisateur

        except Exception as erreur:
            print("Erreur lors de la recherche :", erreur)
            return None

    def delete_by_id(self, id_element):
        """Supprime un utilisateur par son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        try:
            cursor = db.cursor()

            sql = """
             DELETE FROM utilisateur
             WHERE id_utilisateur = %s
             """

            cursor.execute(sql, (id_element,))
            db.commit()

            resultat = cursor.rowcount > 0

            cursor.close()

            return resultat

        except Exception as erreur:
            db.rollback()
            print("Erreur lors de la suppression :", erreur)
            return False

    def ajouter(self, intervention):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
            INSERT INTO intervention
            (description, date_intervention, id_incident, id_utilisateur)
            VALUES (%s, %s, %s, %s)
            """

            valeurs = (
                intervention.description,
                intervention.date_intervention,
                intervention.id_incident,
                intervention.id_utilisateur
            )

            cursor.execute(sql, valeurs)
            db.commit()

            print("Intervention ajoutée avec succès !")

            cursor.close()
            db.close()

    def afficher_toutes(self):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM intervention
            ORDER BY id_intervention DESC
            """

            cursor.execute(sql)

            interventions = cursor.fetchall()

            cursor.close()
            db.close()

            return interventions
        return []

    def afficher_par_incident(self, id_incident):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM intervention
            WHERE id_incident = %s
            ORDER BY date_intervention DESC
            """

            cursor.execute(sql, (id_incident,))

            interventions = cursor.fetchall()

            cursor.close()
            db.close()

            return interventions
        return []

    def ajouter_intervention(self, id_incident, id_utilisateur, description, duree):

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
            INSERT INTO intervention
            (description, date_intervention, id_incident, id_utilisateur, duree)
            VALUES (%s, NOW(), %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    description,
                    id_incident,
                    id_utilisateur,
                    duree
                )
            )

            db.commit()

            print("Intervention ajoutée avec succès !")

            cursor.close()
            db.close()

    def nombre_interventions(self):

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM intervention
            """)

            nombre = cursor.fetchone()[0]

            cursor.close()
            db.close()

            return nombre

        return 0
