
from ..config import db


def create_review(review_data):

    review_data_dict = review_data.dict()
    new_review_ref = db.collection('Review').document()
    new_review_ref.set(review_data_dict)

    return new_review_ref.id
def get_plate_reviews():
    
    try:
        plate_ref = db.collection('Review')
        plate = plate_ref.stream()
        plate_list = []

        for plate in plate:
            plate_dict = plate.to_dict()
            plate_dict['id'] = plate.id
            plate_list.append(plate_dict)
            
        return plate_list
    except Exception as e:
        return {"error": str(e)}, 500

def update_Review(review_id, review_data):
    try:
        updated_data = review_data.dict()
        Plate_ref = db.collection('Review').document(review_id)
        Plate_ref.update(updated_data)

        return "Review updated successfully"
    except Exception as e:
        return {"error": str(e)}
def getamountFiveStarReviews(id_user):
    try:
        # Step 1: Fetch all plates created by the user
        plates_ref = db.collection('Plate').where('id_User', '==', id_user)
        plates = plates_ref.stream()

        # Collect all plate IDs owned by the user
        user_plate_ids = [plate.id for plate in plates]

        # Edge case: If user has no plates
        if not user_plate_ids:
            return 0

        # Step 2: Count five-star reviews for user's plates
        five_star_count = 0
        reviews_ref = db.collection('Review')

        for plate_id in user_plate_ids:
            # Query the Review collection for reviews with a high score for each plate
            reviews = reviews_ref.where('plate_Id', '==', plate_id).stream()
            for review in reviews:
                review_dict = review.to_dict()
                if review_dict.get('score', 0) >= 4:
                    five_star_count += 1
                    break  # Count each plate only once for 4.5+ rating
        return five_star_count
    
    except Exception as e:
        return {"error": str(e)}


    
