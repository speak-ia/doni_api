import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth

FIREBASE_CONFIG = {
        "apiKey": "AIzaSyDaA4vxzVEhDoPMkPk_GgyaeoJivXXEbgs",
        "authDomain": "project-data-3518e.firebaseapp.com",
        "projectId": "project-data-3518e",
        "storageBucket": "project-data-3518e.firebasestorage.app",
        "messagingSenderId": "1017548587806",
        "appId": "1:1017548587806:web:e79417855a39fe547fff0f",
        "databaseURL":""
}

# Initialisation de Pyrebase
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth_pyrebase = firebase.auth()

# Initialisation de Firebase Admin
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("/home/mohpython/Documents/web_project/djangoProject/doni_data/project-data-3518e-firebase-adminsdk-o70gi-8b1f71c08e.json")
    firebase_admin.initialize_app(cred)

def get_firebase_token():
    try:
        email = "speakaboutai@gmail.com"
        password = "password123"
        
        user = auth_pyrebase.sign_in_with_email_and_password(email, password)
        token = user['idToken']
        print("Votre token Firebase :")
        print(f"Bearer {token}")
        return token
    except Exception as e:
        print(f"Erreur d'authentification : {e}")
        return None

if __name__ == "__main__":
    # Test de la fonction
    get_firebase_token()
