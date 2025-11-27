from app.service.review_service import create_review,update_Review,get_plate_reviews,getamountFiveStarReviews
from app.models.review import Review, Comment
from fastapi import HTTPException
from datetime import datetime
from typing import List
 

def validate_comments(comments: List[Comment], current_user_id: str):
    for comment_data in comments:
        if comment_data.score is None or comment_data.score <= 0:
            raise HTTPException(
                status_code=400, 
                detail="Cada comentario debe tener una puntuación (score) válida mayor a 0."
            )
        if not comment_data.comment or not comment_data.comment.strip():
             raise HTTPException(
                status_code=400, 
                detail="Cada comentario debe tener texto y no puede estar vacío."
            )
        if comment_data.id_User != current_user_id:
            raise HTTPException(
                status_code=403, 
                detail="Error de autorización. El ID de usuario en el comentario no coincide con el usuario autenticado."
            )

    return True

def reviewLog(review: Review, user_id:str):
    validate_comments(review.comment, user_id)
    try:
        review_id = create_review(review)
        return {"message": "User review registered successfully", "id": review_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def UpdateReview(review_id: str, updated_data: Review, user_id:str):
    validate_comments(updated_data.comments, user_id)
    try:
        message = update_Review(review_id, updated_data)
        return {"Review": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def get_plateReviews():
    response = get_plate_reviews()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"Review": response}
def get_fiveStarReview(user_id: str):
    response = getamountFiveStarReviews(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response