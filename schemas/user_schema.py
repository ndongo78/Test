

def UserSchema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "address": user["address"],
        "phone": user["phone"],
        "email": user["email"],
        #"password": user["password"],
    }
