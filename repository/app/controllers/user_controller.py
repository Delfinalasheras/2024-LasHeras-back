from app.service.user_service import update_uservalidation, get_allusers, create_user, delete_user, reset_password, get_user_by_id, get_user_by_email, send_password_reset_email, login_user, get_current_user_service, update_user, complete_goal
from app.models.user import UserGoals, UserLogin, ResetPassword, UserRegister, UserForgotPassword, UpdateUserData
from fastapi import HTTPException, Request
import re
from datetime import datetime


def validate_name(campo, label):
    if not campo.strip():
        raise HTTPException(
            status_code=400, detail=f"{label} cannot be empty or blank")
    if type(campo) is not str:
        raise HTTPException(
            status_code=400, detail=f"{label} must be an integer")
    if not re.match(r'^[a-zA-Z\s]+$', campo):
        raise HTTPException(
            status_code=400, detail=f"Invalid format for {label}. Only letters and spaces allowed.")


def validate_limit(campo, minimo, maximo, label):
    if type(campo) is not float:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a float")
    if not (minimo <= campo <= maximo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be between {minimo} and {maximo}.")


def validate_date(date, label):
    if date.date() >= datetime.now().date():
        raise HTTPException(
            status_code=400, detail=f"{label} must be a date in the past.")


def validate_data_user(user_data: UpdateUserData | UserRegister):

    # Validar que los campos de texto no estén vacíos y no tengan caracteres especiales
    validate_name(user_data.name, 'name')
    validate_name(user_data.surname, 'surname')

    # Validar peso y altura (ya asegurado por Pydantic, pero lo reforzamos)
    validate_limit(user_data.weight, 0, 500, 'Weight')
    validate_limit(user_data.height, 0, 500, 'Height')

    # Validar que la fecha de nacimiento sea anterior a hoy
    validate_date(user_data.birthDate, 'Birthdate')

    # Validar los objetivos (goals)
    if any(goal < 0 for goal in vars(user_data.goals).values()):
        raise HTTPException(
            status_code=400, detail="All goals must be greater or equal to 0.")

    if type(user_data.validation) is not int:
        raise HTTPException(
            status_code=400, detail="Validation must be an integer")

    # Validar que los logros (achievements) sean una lista de enteros
    if not all(isinstance(achievement, int) for achievement in user_data.achievements):
        raise HTTPException(
            status_code=400, detail="Achievements must be a list of integers.")

    return True


def login(user: UserLogin):
    return login_user(user)
# Controlador para registrar un nuevo usuario


def userLog(user: UserRegister):
    validate_data_user(user)
    response = create_user(user)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "User registered successfully"}


def delete_user_by_id(user_id: str):
    response = delete_user(user_id)
    return {"message": response}


def resetPassword(reset: ResetPassword):
    response = reset_password(reset)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Password change successfully"}


# Controlador para recuperación de contraseña
def forgot_password(user: UserForgotPassword):
    db_user = user_by_email(user.email)

    if db_user:  # If user exists in Firestore
        return send_password_reset_email(user.email)
    else:
        raise HTTPException(status_code=404, detail="Email not found")


def user_by_email(email: str):
    response = get_user_by_email(email)

    # If user not found, get_user_by_email returns None
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")

    # If an error occurred during the query
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response


def user_by_id(user_id: str):
    response = get_user_by_id(user_id)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")

    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response


def login_user_controller(user: UserLogin):
    response = login_user(user)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Log in succesful"}


def get_current_user(request: Request):
    response = get_current_user_service(request)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Log in succesful"}


def update_user_info(user_id: str, user_data: UpdateUserData):
    verification = get_user_by_id(user_id)
    if not verification:
        raise HTTPException(status_code=404, detail="User not found")
    if (validate_data_user(user_data)):
        response = update_user(user_id, user_data)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
    return response


def get_all_Users():
    response = get_allusers()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response


def update_user_validation(user_id: str):
    verification = get_user_by_id(user_id)
    if (verification):
        response = update_uservalidation(user_id)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        return response


def addGoal(user_id: str, goal_id: int):
    response = complete_goal(user_id, goal_id)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
