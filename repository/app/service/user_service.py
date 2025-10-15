from ..config import db, auth, verify_token
import requests
import os
from dotenv import load_dotenv
from app.service.review_service import getamountFiveStarReviews
from datetime import datetime
from app.models.user import UserRegister

load_dotenv()
api_key = os.getenv('FIREBASE_API_KEY')


def login_user(user_data):
    try:
        # Use Firebase Admin SDK to verify user credentials (email & password)
        user = auth.get_user_by_email(user_data.email)  # Get user by email

        # Verify the password (you may want to handle password checking with Firebase)
        # Unfortunately, Firebase Admin SDK doesn't support login directly, so use the REST API.
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}'
        payload = {
            "email": user_data.email,
            "password": user_data.password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error if the request failed

        # If login is successful, Firebase returns the user data
        user_data = response.json()
        return {"message": "Login successful", "user": user_data}
    except Exception as e:
        return {"error": str(e)}

# Crear un nuevo usuario en Firestore


def create_user(user_data: UserRegister):
    try:
        user_ref = db.collection('User').document(
            user_data.id_user)  # Usa id_user como ID del documento
        user_ref.set({
            "id_user": user_data.id_user,
            "name": user_data.name,
            "surname": user_data.surname,
            "weight": user_data.weight,
            "height": user_data.height,
            "birthDate": user_data.birthDate,
            "goals": user_data.goals.dict(),  # Convierte UserGoals a diccionario
            "validation": user_data.validation,
            "achievements": user_data.achievements,
            "allergies": user_data.allergies,
        })

        return {"message": "User created and data saved successfully"}
    except Exception as e:
        return {"Eror create_user in user_service.py": str(e)}


def delete_user(user_id):
    try:
        user_ref = db.collection('User').where(
            'id_user', '==', user_id).stream()
        user_doc = None

        for doc in user_ref:
            user_doc = doc

        if user_doc:
            user_doc.reference.delete()
            related_collections = ['Category', 'Drink', 'UserFood']

            for collection_name in related_collections:
                collection_ref = db.collection(collection_name).where(
                    'id_User', '==', user_id).stream()
                for doc in collection_ref:
                    doc.reference.delete()

            related_collections = ['DrinkType',  'Schedule', 'UserTotalCal']
            for collection_name in related_collections:
                collection_ref = db.collection(collection_name).where(
                    'id_user', '==', user_id).stream()
                for doc in collection_ref:
                    doc.reference.delete()

            collection_ref = db.collection('UserNotifications').where(
                'user_id', '==', user_id).stream()
            for doc in collection_ref:
                doc.reference.delete()

            try:
                auth.delete_user(user_id)
                print(
                    f"Usuario con UID {user_id} eliminado correctamente de Firebase Authentication.")
            except Exception as e:
                print(
                    f"Error al eliminar usuario en Firebase Authentication: {str(e)}")
                return {"error": "Failed to delete user from Firebase Authentication."}
        else:
            return {"error": "User not found"}

    except Exception as e:
        return {"error": str(e)}


def reset_password(reset):
    try:
        # Verificar el token enviado
        decoded_token = auth.verify_id_token(reset.token)
        user_id = decoded_token['uid']

        # Cambiar la contraseña del usuario en Firebase Authentication
        auth.update_user(user_id, password=reset.new_password)
        return {"message": "Password reset successfully"}
    except Exception as e:
        return {"error": str(e)}


def get_user_by_email(email):
    try:
        users_ref = db.collection('User')
        query = users_ref.where('email', '==', email).stream()

        for user in query:
            return user.to_dict()  # If user is found, return user data as a dictionary

        return None  # Return None if no user is found
    except Exception as e:
        return {"error": str(e)}


def get_user_by_id(user_id):
    try:
        user_ref = db.collection('User')
        query = user_ref.where('id_user', '==', user_id).stream()

        for user in query:
            return user.to_dict()  # If user is found, return user data as a dictionary

        return None
    except Exception as e:
        return {"error": str(e)}


def send_password_reset_email(email):
    # Firebase Auth REST API URL
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}'

    # API Key is required here. Replace `YOUR_API_KEY` with your Firebase project's API key.
    payload = {
        'requestType': 'PASSWORD_RESET',
        'email': email
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.json().get('email'):
            return {'message': 'Password reset email sent! Please check your inbox'}
        else:
            return {'message': 'Unexpected response from Firebase'}

    except requests.exceptions.HTTPError as err:
        return {'error': f'Error during password reset: {err}'}


def update_user(user_id, user_data):
    try:
        updated_data = user_data.dict()
        user_ref = db.collection('User').where(
            'id_user', '==', user_id).stream()
        print(updated_data)

        for doc in user_ref:
            doc.reference.update(updated_data)
            print("User data updated successfully")
            return {"message": "User data updated successfully"}

    except Exception as e:
        print(e)
        return {"error": str(e)}


def get_current_user_service(request):
    token = request.headers.get('Authorization').split("Bearer ")[1]
    decoded_token = verify_token(token)
    return decoded_token


def update_uservalidation(user_id):
    try:
        count_verified_plates = getamountFiveStarReviews(user_id)
        level = ""

        if count_verified_plates >= 5:
            level = 2
        elif count_verified_plates >= 3:
            level = 1
        else:
            level = 0

        user = get_user_by_id(user_id)
        if level == user['validation']:
            return {"Updated"}
        else:
            user_ref = db.collection('User').where(
                'id_user', '==', user_id).stream()
            user_notify(user, level)
            user['validation'] = level

            for doc in user_ref:
                doc.reference.update(user)

            return {"Updated"}
    except Exception as e:
        return {"error": str(e)}


def get_allusers():
    try:
        users_ref = db.collection('User').stream()
        users = []

        for doc in users_ref:
            user_data = doc.to_dict()
            users.append(user_data)

        return users

    except Exception as e:
        return {"error": str(e)}


def user_notify(user, new_level):
    last_notified_level = user.get('validation', 0)
    user_id = user.get('id_user')
    if user_id is None:
        print("Error: User ID not found.")
        return {"error": "User ID not found"}

    if new_level > last_notified_level:
        message = f"Congratulations! You've reached level {new_level} verification."
    else:
        message = f"Your verification level has changed to {new_level}."

    # Use datetime.now() to test if SERVER_TIMESTAMP is the issue
    data = {
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now(),  # Temporarily replace with datetime.now()
        'is_read': False
    }

    try:
        new_review_ref = db.collection('UserNotifications').document()
        new_review_ref.set(data)

    except Exception as e:

        return {"error": str(e)}

    return {"notification": "Notification sent"}


def notifyUserAchievement(message, user_id):
    data = {
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now(),
        'is_read': False
    }

    try:
        new_review_ref = db.collection('UserNotifications').document()
        new_review_ref.set(data)
    except Exception as e:
        print(f"Error sending notification: {e}")
        return {"error": str(e)}

    return {"notification": "Notification sent"}


def complete_goal(user_id, goal_id):
    try:
        # Retrieve the user document
        user_ref = db.collection('User').where(
            'id_user', '==', user_id).stream()

        # Extract user data from query result
        user_doc = next(user_ref, None)
        if not user_doc:
            return {"error": "User not found"}

        user_data = user_doc.to_dict()

        # Initialize achievements if they don't exist
        achievements = user_data.get('achievements', [])

        # Only add if not already in the list
        if goal_id not in achievements:
            achievements.append(goal_id)
            user_doc.reference.update({'achievements': achievements})
            message = "Congratulations! You achieved a new goal!"
            result = notifyUserAchievement(message, user_id)

            if "error" in result:
                return {"error": f"Notification error: {result['error']}"}

    except Exception as e:
        return {"error": str(e)}

    return {"message": "Goal completed and notification sent"}
