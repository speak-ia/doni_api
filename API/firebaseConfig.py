import os
import pyrebase

FIREBASE_CONFIG = {
        "apiKey": "AIzaSyDaA4vxzVEhDoPMkPk_GgyaeoJivXXEbgs",
        "authDomain": "project-data-3518e.firebaseapp.com",
        "projectId": "project-data-3518e",
        "storageBucket": "project-data-3518e.appspot.com",
        "messagingSenderId": "1017548587806",
        "appId": "1:1017548587806:web:e79417855a39fe547fff0f",
        "databaseURL": ""
    
}
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()
