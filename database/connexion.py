import mysql.connector
from database.config import *

class Connexion:

    __instance = None

    @staticmethod
    def get_instance():
        if Connexion.__instance is None:
            Connexion()
        return Connexion.__instance

    def __init__(self):

        if Connexion.__instance is not None:
            raise Exception("Connexion déjà créée")

        self.conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        Connexion.__instance = self

    def get_connexion(self):
        return self.conn