from firebaseConfig import auth

def get_firebase_token():
    try:
        # Remplacez par vos identifiants de test
        email = "speakaboutai@gmail.com"
        password = "password123"
        
        # Authentification avec Firebase
        user = auth.sign_in_with_email_and_password(email, password)
        
        # Obtenir le token ID
        token = user['idToken']
        print("Votre token Firebase :")
        print(token)
        return token
    except Exception as e:
        print(f"Erreur d'authentification : {e}")
        return None

if __name__ == "__main__":
    get_firebase_token() 