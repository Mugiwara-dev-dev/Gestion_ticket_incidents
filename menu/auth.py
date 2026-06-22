from dao.utilisateur_dao import UtilisateurDAO

def connexion():

    login = input("Login : ")
    password = input("Mot de passe : ")

    dao = UtilisateurDAO()

    utilisateur = dao.authentifier(login, password)

    if utilisateur:
        print("Connexion réussie")
        return utilisateur

    print("Login ou mot de passe incorrect")
    return None