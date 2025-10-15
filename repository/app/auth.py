from firebase_admin import auth
from fastapi import HTTPException
from firebase_admin.auth import verify_id_token


def validate_user_id(token: str, id_user: str):
    try:
        decoded_token = verify_id_token(token)
        firebase_uid = decoded_token["uid"]
        if firebase_uid != id_user:
            raise HTTPException(
                status_code=400,
                detail="id_user does not match the authenticated user's ID"
            )
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Authentication failed: {str(e)}"
        )

