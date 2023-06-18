


def CategorySchema(category)->dict:
  return {
     "_id": str(category["_id"]),
     "name": category["name"]
  }