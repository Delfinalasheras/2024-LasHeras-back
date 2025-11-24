import firebase_admin
from firebase_admin import credentials, firestore, auth
from fastapi import HTTPException
import os
import json
from dotenv import load_dotenv

load_dotenv()

if not firebase_admin._apps:
    firebase_cred_json = os.getenv('FIREBASECREDENTIALS')
    firebase_creds_dict = json.loads(firebase_cred_json)

    cred = credentials.Certificate(firebase_creds_dict)
    firebase_admin.initialize_app(cred)


db = firestore.client()

auth = firebase_admin.auth

def verify_token(auth_header: str):
    try:
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization header format")

        token = auth_header.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token

    except Exception as e:
        print("Error en verify_token:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")


