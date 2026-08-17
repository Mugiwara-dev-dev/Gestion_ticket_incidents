from database.connexion import Connexion
from dao.base_dao import BaseDAO

class UtilisateurDAO(BaseDAO):

    def get_all(self):
        """Retourne la liste de tous les utilisateurs."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
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
                print(
                    "Erreur lors de la récupération des utilisateurs :",
                    erreur
                )
                return []

        return []

    def get_by_id(self, id_element):
        """Retourne un utilisateur à partir de son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
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
                print(
                    "Erreur lors de la recherche de l'utilisateur :",
                    erreur
                )
                return None

        return None

    def delete_by_id(self, id_element):
        """Supprime un utilisateur à partir de son identifiant."""

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            try:
                cursor = db.cursor()

                sql = """
                DELETE FROM utilisateur
                WHERE id_utilisateur = %s
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
                    "Erreur lors de la suppression de l'utilisateur :",
                    erreur
                )

                return False

        return False


    def authentifier(self, login, mot_de_passe):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM utilisateur
            WHERE login = %s
            AND mot_de_passe = %s
            """

            cursor.execute(sql, (login, mot_de_passe))

            utilisateur = cursor.fetchone()

            cursor.close()
            db.close()

            return utilisateur
        return None

    def rechercher_par_id(self, id_utilisateur):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM utilisateur
            WHERE id_utilisateur = %s
            """

            cursor.execute(sql, (id_utilisateur,))

            utilisateur = cursor.fetchone()

            cursor.close()
            db.close()

            return utilisateur
        return None

    def modifier_utilisateur(
            self,
            id_utilisateur,
            nom,
            prenom,
            login,
            mot_de_passe,
            role
    ):
        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
            UPDATE utilisateur
            SET nom = %s,
                prenom = %s,
                login = %s,
                mot_de_passe = %s,
                role = %s
            WHERE id_utilisateur = %s
            """

            cursor.execute(
                sql,
                (
                    nom,
                    prenom,
                    login,
                    mot_de_passe,
                    role,
                    id_utilisateur
                )
            )

            if cursor.rowcount > 0:
                db.commit()
                print("Utilisateur modifié avec succès !")
            else:
                print("Utilisateur introuvable.")

            cursor.close()
            db.close()

    def supprimer_utilisateur(self, id_utilisateur):

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            # Vérifier si l'utilisateur possède des incidents
            sql_incidents = """
            SELECT COUNT(*)
            FROM incident
            WHERE id_utilisateur = %s
            """

            cursor.execute(sql_incidents, (id_utilisateur,))
            nb_incidents = cursor.fetchone()[0]

            # Vérifier si l'utilisateur possède des interventions
            sql_interventions = """
            SELECT COUNT(*)
            FROM intervention
            WHERE id_utilisateur = %s
            """

            cursor.execute(sql_interventions, (id_utilisateur,))
            nb_interventions = cursor.fetchone()[0]

            if nb_incidents > 0 or nb_interventions > 0:

                print("Impossible de supprimer cet utilisateur.")

                if nb_incidents > 0:
                    print("Cet utilisateur possède des incidents.")

                if nb_interventions > 0:
                    print("Cet utilisateur possède des interventions.")

            else:

                sql_delete = """
                DELETE FROM utilisateur
                WHERE id_utilisateur = %s
                """

                cursor.execute(sql_delete, (id_utilisateur,))

                if cursor.rowcount > 0:
                    db.commit()
                    print("Utilisateur supprimé avec succès !")
                else:
                    print("Utilisateur introuvable.")

            cursor.close()
            db.close()

    def rechercher_utilisateur(self, recherche):

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor(dictionary=True)

            sql = """
            SELECT *
            FROM utilisateur
            WHERE nom LIKE %s
               OR prenom LIKE %s
               OR login LIKE %s
            ORDER BY nom
            """

            valeur = "%" + recherche + "%"

            cursor.execute(
                sql,
                (valeur, valeur, valeur)
            )

            utilisateurs = cursor.fetchall()

            cursor.close()
            db.close()

            return utilisateurs
        return []

    def ajouter_utilisateur(
            self,
            nom,
            prenom,
            login,
            mot_de_passe,
            role
    ):

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            sql = """
            INSERT INTO utilisateur
            (nom, prenom, login, mot_de_passe, role)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    nom,
                    prenom,
                    login,
                    mot_de_passe,
                    role
                )
            )

            db.commit()

            print("Utilisateur ajouté avec succès !")

            cursor.close()
            db.close()

    def nombre_utilisateurs(self):

        connexion = Connexion()
        db = connexion.connecter()

        if db:
            cursor = db.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM utilisateur
            """)

            nombre = cursor.fetchone()[0]

            cursor.close()
            db.close()

            return nombre
        return 0

    if __name__ == "__main__":
        dao = UtilisateurDAO()

        print("UtilisateurDAO fonctionne correctement.")