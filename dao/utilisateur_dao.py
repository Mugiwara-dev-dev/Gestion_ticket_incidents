from database.connexion import Connexion

class UtilisateurDAO:

    def __init__(self):
        self.conn = Connexion.get_instance().get_connexion()

    def authentifier(self, login, password):

        cursor = self.conn.cursor(dictionary=True)

        requete = """
        SELECT *
        FROM utilisateur
        WHERE login=%s
        AND password=%s
        """

        cursor.execute(requete, (login, password))

        return cursor.fetchone()