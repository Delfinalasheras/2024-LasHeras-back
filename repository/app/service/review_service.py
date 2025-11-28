
from ..config import db
from app.models.review import Comment


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

def add_comment_logic(review_id: str, new_comment: Comment):
    try:
        plate_ref = db.collection('Review').document(review_id)
        doc = plate_ref.get()

        if not doc.exists:
            raise Exception("La review/plato no existe")

        data = doc.to_dict()
        current_comments = data.get('comments', [])
        new_comment_dict = new_comment.dict()
        current_comments.append(new_comment_dict)

        total_score = sum(c['score'] for c in current_comments)
        new_average = total_score / len(current_comments)
        new_average = round(new_average, 1)
        plate_ref.update({
            "comments": current_comments,
            "score": new_average
        })

        return {"Comentario agregado y score actualizado exitosamente para el usuario",new_comment.id_User}

    except Exception as e:
        # Es buena práctica loggear el error real
        print(f"Error updating review: {e}")
        raise e
def getamountFiveStarReviews(id_user):
    try:
        plates_ref = db.collection('Plate').where('id_User', '==', id_user)
        plates = plates_ref.stream()
        user_plate_ids = [plate.id for plate in plates]

        if not user_plate_ids:
            return 0
        five_star_count = 0
        reviews_ref = db.collection('Review')

        for plate_id in user_plate_ids:
            reviews = reviews_ref.where('plate_Id', '==', plate_id).stream()
            for review in reviews:
                review_dict = review.to_dict()
                if review_dict.get('score', 0) >= 4:
                    five_star_count += 1
                    break 
        return five_star_count
    
    except Exception as e:
        return {"error": str(e)}


    
