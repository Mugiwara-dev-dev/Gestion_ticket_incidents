from menu.auth import connexion

user = connexion()

if user:

    print("Bienvenue",
          user["prenom"],
          user["nom"])

    print("Rôle :", user["role"])