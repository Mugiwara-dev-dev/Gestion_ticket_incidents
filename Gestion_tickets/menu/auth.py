from dao.utilisateur_dao import UtilisateurDAO
from menu.interface import Interface

class Auth:

    def se_connecter(self):
        print()
        print("======================================")
        print("             CONNEXION")
        print("======================================")

        login = input("Login : ")
        mot_de_passe = input("Mot de passe : ")

        dao = UtilisateurDAO()

        utilisateur = dao.authentifier(login, mot_de_passe)

        if utilisateur:
            print()
            print("Bienvenue", utilisateur["prenom"], utilisateur["nom"])
            print("Rôle :", utilisateur["role"])

            interface = Interface()
            interface.lancer(utilisateur)

            return utilisateur

        print()
        print("Login ou mot de passe incorrect.")
        return None