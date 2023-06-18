

def ArticleSchema(article)->dict:
    return{
      "_id": str(article["_id"]),
      "title": article["title"],
      "description": article["description"],
      "price": article["price"],
      "category_id": article["category_id"],
      "image": article["image"]

    }