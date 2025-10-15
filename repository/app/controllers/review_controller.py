from app.service.review_service import create_review,update_Review,get_plate_reviews,getamountFiveStarReviews
from app.models.review import Review
from fastapi import HTTPException
from datetime import datetime


def reviewLog(review: Review):
    try:
        review_id = create_review(review)
        return {"message": "User review registered successfully", "id": review_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def UpdateReview(review_id: str, updated_data: Review):
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