from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File

from models.article_model import Article
from db.database import Database 
from schemas.article_schema import ArticleSchema

from bson import ObjectId 
import os

article_router =APIRouter()

article_collection =Database.db.get_collection("article")

import os

# Fonction de recherche du fichier
def search_file(file_path):
    # Vérifier si le fichier existe
    if os.path.exists(file_path):
        return file_path
    else:
        return None
#save image dans les image
async def upload_image(image):
    image_type= image.content_type

    if image_type not in ["image/jpg","image/png","image/jpeg"]:
      raise HTTPException(status_code=400, detail="Seul les images sont autorisées")

    
    # Enregistrer l'image
    _,extension = os.path.splitext(image.filename)
    image_data = await image.read()
    image_id = str(ObjectId())
    image_path = f"images/{image_id}{extension}"
    
    with open(image_path, "wb") as f:
        f.write(image_data)
    
    return image_path
 




@article_router.get("/")
async def get_articles():
    articles= []
    async for article in article_collection.find():
        articles.append(ArticleSchema(article))
    return articles

@article_router.post('/')
async def create_article(title: str, description: str, price: float, category_id: str, image: UploadFile):
    # Créer une instance de l'article
    article = Article(
        title=title,
        description=description,
        price=price,
        category_id=category_id
    )
    # Ajouter le chemin de l'image à l'article
    image_path= await upload_image(image)
    article.image = image_path
    # Enregistrer l'article dans la base de données
    article_data = article.dict()
    result = await article_collection.insert_one(article_data)
    
    return {
        'message': 'Article enregistré avec succès',
        'article_id': str(result.inserted_id)
    }

 
@article_router.put('/')
async def update_article(id:str,title:str,description:str,price:float,category_id:str, image:UploadFile=None):
  article_current= await article_collection.find_one({"_id":ObjectId(id)})
  if image is not None:
    currentImg= search_file(article_current["image"])
    if currentImg is not None:
       os.remove(currentImg)
       image_path= upload_image(image)
       article = Article(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        image= image_path
       ) 
       newArticle= await article_collection.update_one({"_id":ObjectId(id)},{"$set":dict(article)})
       return {"message": "Mise à jour effectuée avec succès"}
    else:
      articleUpdated= Article(
       title=title,
       description= description,
       price= price,
       category_id= category_id,
       image= article_current["image"]
      )
      artToSave= await article_collection.update_one({"_id":ObjectId(id)},{"$set":dict(articleUpdated)})

      return {"message": "Mise à jour effectuée avec succès"}


@article_router.delete("/")
async def ddeletearticle(id: str):
  article= await article_collection.find_one({"_id": ObjectId(id)})
  if article is not None:
    imageDelete= search_file(article["image"])
    if imageDelete is not None:
       os.remove(str(imageDelete))
       await article_collection.delete_one({"_id":ObjectId(id)})
       return {"message": "article supprimé avec succès","path":imageDelete}
    else:
       return {"message": "Pas d'image dans le folder"}
   


        

