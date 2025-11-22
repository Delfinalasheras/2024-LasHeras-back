from fastapi import APIRouter, Depends, Request, HTTPException
from app.models.food import Food
from app.controllers.user_controller import userLog,addGoal,update_user_info, delete_user_by_id, user_by_id, resetPassword,update_user_validation,get_all_Users
from app.controllers.userTotCal_controller import get_totcal_day,updateDailyCalories_controller, createUserTotCal, get_TotCal, get_streak
from app.controllers.food_controller import register_new_food, get_foods, get_food_by_id
from app.controllers.recomendations_controller import get_recommendations
from app.controllers.category_controller import userCategoryLog, get_category, update_category_controller, delete_category
from app.controllers.catFood_controller import CategoryFoodLog, get_Food_perCat, delete_Catfood, delete_AllCatfoodByCategory
from app.controllers.plate_controller import get_publicPlates_notUser,update_user_plates_to_verified,plateLog, get_plate_user, delete_plate, update_Plate, get_platebyID, get_publicPlates
from app.controllers.plateFood_controller import PlateFoodLog, update_PlateFood_controller, delete_PlateFood, get_plateFood
from app.controllers.drinkType_controller import register_new_drinkType, get_drinkTypes, get_drinkType_by_id, UserDrinkTypes, delete_DrinkType
from app.controllers.review_controller import reviewLog, UpdateReview, get_plateReviews, get_fiveStarReview
from app.controllers.notification_controller import getNotis,NotificationRead
from app.models.user import UserRegister,GoalRequest, ResetPassword, UserForgotPassword, UserLogin, UpdateUserData
from app.controllers.drink_controller import register_new_drink, get_drinks, get_drink_by_id, deletedrink, Updatedrink, Grouped_Drinks
# from app.controllers.user_controller import
from app.models.catFood import CategoryFood
from app.models.category import Category
from app.models.userFood import UserFood
from app.models.plate import Plate
from app.models.drink import Drink
from app.models.drinkType import DrinkType
from app.models.review import Review
from app.models.plateFood import PlateFood
from app.models.userTotCal import UserTotCal, CalUpdateModel
from app.controllers.foodUser_controller import update_userFood_controller, userFoodLog, get_meals_user, delete_meal
from datetime import datetime
from .config import verify_token
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from app.auth import validate_user_id
from firebase_admin import auth as firebase_auth
from app.models.weeklyPlan import WeeklyPlanRequest
from app.controllers.weeklyPlan_controller import get_weekly_plan_controller, update_weekly_plan_controller,get_shoppingList
from app.controllers.dailyPlan_controller import get_or_build_menu
auth_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

def get_token_from_header(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    return auth_header.split(" ")[1]


def get_current_user(token: str = Depends(get_token_from_header)):
    print("🔒 Token verification called")
    try:
        decoded = firebase_auth.verify_id_token(token)
        uid = decoded.get("user_id") or decoded.get("uid")
        if not uid:
            raise Exception("user_id not in token")
        return {"uid": uid, "decoded": decoded}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# Simple root endpoint
@router.get("/", tags=["General"])
def read_main(current_user: dict = Depends(get_current_user)):
    return {"msg": f"Server is running for user {current_user['uid']}"}


# User endpoints
@router.post("/RegisterUser", tags=["User"])
async def register_user(user: UserRegister, current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]
    response = userLog(user, user_id)

    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return {"message": "User registered successfully!"}



@router.get("/getUser", tags=["User"])
async def get_user(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    response = user_by_id(user_id)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": response}


@router.put("/update_user", tags=["User"])
async def update_user_data(user_data: UpdateUserData, current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]
    update_user_info(user_id, user_data)
    return {"message": "User data updated successfully!"}


@router.delete("/delete_user", tags=["User"])
async def delete_user(current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]
    delete_user_by_id(user_id)
    return {"message": "User deleted successfully!"}


# Foods
@router.post("/Food_log", tags=["Food"])
async def register_food(Food: Food, current_user: dict = Depends(get_current_user)):
    register_new_food(Food)
    return {"message": "Food log added!"}


@router.get("/Foods", tags=["Food"])
async def read_food_logs(current_user: dict = Depends(get_current_user)):
    return get_foods()


@router.get("/Foods/{food_id}", tags=["Food"])
async def get_food(food_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_food_by_id(user_id, food_id)


# User Foods (Meals)
@router.post("/UserFood_log", tags=["MealUser"])
async def register_foodMeal(FoodUser: UserFood, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    if FoodUser.id_User != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    userFoodLog(FoodUser)
    return {"message": "Meal log added!"}


@router.get("/mealUserDay", tags=["MealUser"])
async def get_meal(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    response = user_by_id(user_id)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return get_meals_user(user_id)


@router.delete("/DeleteMealUser/{id_UserFood}", tags=["MealUser"])
async def delete_mealUser(id_UserFood: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return delete_meal(user_id, id_UserFood)


@router.put("/UpdateUserFood/{userFood_id}", tags=["MealUser"])
async def update_user_food(userFood_id: str, userFood_data: UserFood, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return update_userFood_controller(user_id, userFood_id, userFood_data)


# Categories
@router.post("/CreateCategory", tags=["Category"])
async def category_log(category: Category, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    userCategoryLog(user_id, category)
    return {"message": "New category!"}


@router.get("/GetCategoryUser", tags=["Category"])
async def get_category_user(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_category(user_id)
@router.get("/GetDefaultCategory/", tags=["Category"])
async def get_default_category():
    return get_category("default")


@router.put("/UpdateCategory/{category_id}", tags=["Category"])
async def update_category(category_id: str, updated_category: Category, current_user: dict = Depends(get_current_user)):
    print("📥 Received category_id:", category_id)
    print("📥 Received updated_category:", updated_category.dict())
    user_id = current_user['uid']
    return update_category_controller(user_id, category_id, updated_category)



# @router.post("/CreateCatFood/", tags=["CatFood"])
# async def category_log(catFood: CategoryFood,current_user: dict = Depends(get_current_user)):
#     CategoryFoodLog(catFood)
#     return {"message": "new categoryFood!"}


# @router.get("/GetFoodsPerCategory/{id_Category}", tags=["CatFood"])
# async def get_Food_Percategory(id_Category: str):
#     return get_Food_perCat(id_Category)


@router.delete("/DeleteCategory/{id_Category}", tags=["Category"])
async def delete_category_user(id_Category: str,current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    delete_category(user_id,id_Category)
    return {"message": "Category Delete Succefully!"}


# @router.delete("/DeleteCatFood/{id_CatFood}", tags=["CatFood"])
# async def delete_catFood_user(id_CatFood: str):
#     delete_Catfood(id_CatFood)
#     return {"message": "CatFood Delete succefully!"}

#CALORIAS TOTALES

@router.post("/CreateTotCaloriesUser/", tags=["Food"])
async def create_tot_cal_user(userTotCal: UserTotCal, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']

    return createUserTotCal(user_id, userTotCal)



@router.put("/UpdateTotCaloriesUser/{calPerDay_id}", tags=["Food"])
async def UpdateUserTotCal_log(calPerDay_id: str, calUpdate: UserTotCal, current_user: dict = Depends(get_current_user)):
    user_id= current_user['uid']
    response = updateDailyCalories_controller(user_id,calPerDay_id, calUpdate)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Update successful!"}


@router.get("/GetTotCalUser/", tags=["Food"])
async def get_Totcal_user( current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_TotCal(user_id)

@router.get("/getTotCalDay/{day}", tags=['Food'])
async def get_Totcal_day(day: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']

    # Convertir string → datetime
    try:
        day_dt = datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD.")

    return get_totcal_day(user_id, day_dt)
# PLATE ROUTES


@router.post("/CreatePlate/", tags=["Plate"])
async def plate_log(plate: Plate, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return plateLog(user_id,plate)


@router.get("/GetPlatesUser/", tags=["Plate"])
async def get_plateuser(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_plate_user(user_id)


@router.get("/GetPlateByID/{plate_id}", tags=["Plate"])
async def get_PlateId(plate_id: str, current_user: dict = Depends(get_current_user)):
    return get_platebyID(plate_id)


@router.get("/GetPlatePublicPlates/", tags=["Plate"])
async def publicPlates(current_user: dict = Depends(get_current_user)):
    return get_publicPlates()


@router.put("/UpdatePlate/{plate_id}", tags=["Plate"])
async def update_category(plate_id: str, updated_Plate: Plate, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return update_Plate(plate_id, updated_Plate)


@router.delete("/DeletePlate/{id_Plate}", tags=["Plate"])
async def delete_plate_user(id_Plate: str,current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return delete_plate(user_id,id_Plate)
# PLATE FOOD


# @router.post("/CreatePlateFood/", tags=["PlateFood"])
# async def plateFood_log(plateFood: PlateFood):
#     return PlateFoodLog(plateFood)


# @router.get("/GetPlateFood/{plateFood_id}", tags=["PlateFood"])
# async def get_plateFood_user(plateFood_id: str):
#     return get_plateFood(plateFood_id)


# @router.put("/UpdatePlateFood/{id_PlateFood}", tags=["PlateFood"])
# async def update_PlateFood(plateFood_id: str, updated_PlateFood: PlateFood):
#     return update_PlateFood_controller(plateFood_id, updated_PlateFood)


# @router.delete("/DeletePlateFood/{id_PlateFood}", tags=["PlateFood"])
# async def delete_plateFood(id_plate: str):
#     delete_PlateFood(id_plate)
#     return {"message": "plate Delete Succefully!"}

# DRINKS


@router.post("/drink_log/", tags=["Drinks"])
async def register_drink(drink: Drink, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    register_new_drink(user_id,drink)
    return {"message": "drink log added!"}


@router.get("/GetDrinks/", tags=["Drinks"])
async def read_drink_logs(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_drinks(user_id)


@router.get("/DrinkById/{drink_id}", tags=["Drinks"])
async def get_drink(drink_id: str, current_user: dict = Depends(get_current_user)):
    return get_drink_by_id(drink_id)


@router.post("/drinkType_log/", tags=["DrinkType"])
async def register_drink(drinkType: DrinkType, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    response = register_new_drinkType(user_id,drinkType)
    return response


@router.get("/getDrinkType/", tags=["DrinkType"])
async def read_drink_logs(current_user: dict = Depends(get_current_user)):
    return get_drinkTypes()


@router.get("/DrinkTypeByID/{drink_id}", tags=["DrinkType"])
async def get_drinkType(drink_id: str, current_user: dict = Depends(get_current_user)):
    return get_drinkType_by_id(drink_id)


@router.get("/getUserDrinkType/", tags=["DrinkType"])
async def get_drinkTypeUser(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return UserDrinkTypes(user_id)


@router.delete("/DeleteDrink/{id_drink}", tags=["Drinks"])
async def delete_drink_user(id_drink: str,current_user: dict = Depends(get_current_user)):

    response = deletedrink(id_drink)
    return {"message": response}


@router.put("/UpdateDrink/{drink_id}", tags=["Drinks"])
async def UpdateUserTotCal_log(drink_id: str, drinkUpdate: Drink, current_user: dict = Depends(get_current_user)):
    response = Updatedrink(drink_id, drinkUpdate)
    return {"message": response}


@router.delete("/DeleteDrinkType/{drinkType_id}", tags=["DrinkType"])
async def deleteDrinktype(drinkType_id: str,current_user: dict = Depends(get_current_user)):
    return delete_DrinkType(drinkType_id)


@router.get("/getUserGroupDrinkType/", tags=["Drink"])
async def get_GroupeddrinkTypeUser(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return Grouped_Drinks(user_id)


@router.post("/newReview/", tags=["Review"])
async def register_newReview(review: Review,current_user: dict = Depends(get_current_user)):
    response = reviewLog(review)
    return response


@router.put("/UpdateReview/{review_id}", tags=["Review"])
async def Update_Review(review_id: str, ReviewUpdate: Review, current_user: dict = Depends(get_current_user)):
    response = UpdateReview(review_id, ReviewUpdate)
    return {"message": response}


@router.get("/PlateReviews/", tags=["Review"])
async def get_reviews():
    return get_plateReviews()


@router.get("/Streak/", tags=["gaminfication"])
async def get_streakuser(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_streak(user_id)


@router.get("/fivestarReview/", tags=["gaminfication"])
async def get_fivestarReviewuser(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_fiveStarReview(user_id)

@router.get("/updateUsersandPlateVerification/", tags=["gamification"])
def scheduled_verification_task():
    users = get_all_Users()
    for user in users:
        update_user_plates_to_verified(user['id_user'])  # Access 'id_user' using dictionary key
        update_user_validation(user['id_user'])
@router.get("/getUserNotifications/",tags=["notis"] )
def getUser_Notifications(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return getNotis(user_id)
@router.put("/markNotificationAsRead/{notification_id}", tags=["Review"])
async def markAsRead(notification_id: str, current_user: dict = Depends(get_current_user)):
    response = NotificationRead(notification_id)
    return {"message": response}
@router.get("/PublicplatesNotFromUser/", tags=['Plate'])
def getNotUser_Publicplates(current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    response = get_publicPlates_notUser(user_id)
    return response
@router.post("/addGoal", tags=['gamification'])
def addGoal_Touser(request: GoalRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    goal_id = request.achivement_id
    response = addGoal(user_id, goal_id)
    return response
@router.get("/getRecomendations/{meal_type}", tags=['Food'])
def get_recomendations(meal_type: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    response = get_recommendations(user_id, meal_type)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response

@router.get("/getOrbuildDailyMenu/{day}", tags=['Food'])
def build_daily_menu_route(day: str,current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    response = get_or_build_menu(user_id,day)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response
@router.get("/weekly-plan/{week_start}", tags=["WeeklyPlan"])
async def get_plan(week_start: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    return get_weekly_plan_controller(user_id, week_start)

@router.patch("/weekly-plan/{week_start}", tags=["WeeklyPlan"])
async def update_plan(
    plan_request: WeeklyPlanRequest, 
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user['uid']

    
    return update_weekly_plan_controller(user_id, plan_request)
@router.get("/shoppingList/{week_start}", tags=["ShoppingList"])
async def get_shopping_list(week_start: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user['uid']
    shopping_list=get_shoppingList(user_id, week_start)
    return shopping_list

