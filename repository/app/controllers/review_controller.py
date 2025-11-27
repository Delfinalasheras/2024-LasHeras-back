from app.service.review_service import create_review,add_comment_logic,get_plate_reviews,getamountFiveStarReviews
from app.models.review import Review, Comment
from fastapi import HTTPException
from datetime import datetime
from typing import List
 

def validate_newReviw(review, current_user_id: str):
    "review.score has to be 0 because is a new plate and the list of comments has to be empty"
    if review.score != 0:
        raise HTTPException(status_code=400, detail="The score of a new review has to be 0")
    if review.comments and len(review.comments) > 0:
        raise HTTPException(status_code=400, detail="The comments list of a new review has to be empty")
    else:
        return True

def reviewLog(review: Review, user_id:str):
    validate_newReviw(review, user_id)
    try:
        review_id = create_review(review)
        return {"message": "User review registered successfully", "id": review_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def UpdateReview(review_id: str, new_comment: Comment):
    try:
        message = add_comment_logic(review_id, new_comment)
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

