import json
from datetime import datetime

from app.Repository.mongo_context import Initializing_Mongo_DB
from app.Models.article import Article
from app.Models.json_web_token_dto import JSON_Web_Token_DTO
from app.Models.encrypted_new_article_dto import Encrypted_New_Article_DTO
from app.Models.encrypted_edit_article_dto import Encrypted_Edit_Article_DTO
from app.Models.encrypted_delete_article_dto import Encrypted_Delete_Article_DTO

from app.Services.authenticate_jwt_claims import Authenticate_JWT_Claims
from app.Services.decryptor import Decryptor
from app.Services.encryptor import Encryptor

from beanie import PydanticObjectId
from fastapi import FastAPI, HTTPException, Body
from fastapi.encoders import jsonable_encoder

from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await Initializing_Mongo_DB()

@app.post("/new/article/", response_model=Article)
async def create_article(dto: Encrypted_New_Article_DTO):

    if not Authenticate_JWT_Claims(dto.token):
        raise HTTPException(status_code=401, detail="Error A")

    try:
        decrypted = {
            "user_id": Decryptor(dto.user_id),
            "language": Decryptor(dto.language),
            "region": Decryptor(dto.region),
            "headline": Decryptor(dto.headline),
            "subheadline": Decryptor(dto.sub_headline),
            "byline": Decryptor(dto.byline),
            "image_urls": json.loads(Decryptor(dto.image_urls)) if dto.image_urls else [],
            "body": json.loads(Decryptor(dto.body)) if dto.body else [],
            "tags": json.loads(Decryptor(dto.tags)) if dto.tags else [],
            "source_urls": json.loads(Decryptor(dto.source_urls)) if dto.source_urls else [],
        }

        article = Article(
            user_id=decrypted["user_id"],
            language=decrypted["language"],
            region=decrypted["region"],
            headline=decrypted["headline"],
            subheadline=decrypted["subheadline"],
            byline=decrypted["byline"],
            deleted=False,
            published_on=int(datetime.utcnow().timestamp() * 1000),
            updated_on=int(datetime.utcnow().timestamp() * 1000),
            image_urls=decrypted["image_urls"],
            body=decrypted["body"],
            tags=decrypted["tags"],
            source_urls=decrypted["source_urls"],
        )

        return await article.create()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error B")

@app.post("/get/articles/")
async def get_all_articles(dto: JSON_Web_Token_DTO):
    if not Authenticate_JWT_Claims(dto.token):
        raise HTTPException(status_code=401, detail="Error C")

    articles = await Article.find(Article.deleted == False).to_list()
    json_ready = jsonable_encoder(articles)
    json_string = json.dumps(json_ready)
    encrypted_string = Encryptor(json_string)
    return encrypted_string

@app.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: PydanticObjectId):
    return await Article.get(article_id)

@app.delete("/delete/article/")
async def soft_delete_article(dto: Encrypted_Delete_Article_DTO = Body(...)):

    if not Authenticate_JWT_Claims(dto.token):
        raise HTTPException(status_code=401, detail="Error D")

    try:
        decrypted_id = Decryptor(dto.article_id)
        article_id = PydanticObjectId(decrypted_id)

        article = await Article.get(article_id)

        if not article:
            raise HTTPException(status_code=404, detail="Error E")

        if article.deleted:
            return article

        article.deleted = True
        article.updated_on = int(datetime.utcnow().timestamp() * 1000)
        await article.save()
        return Encryptor("true")
    except Exception:
        raise HTTPException(status_code=400, detail="Error F")

@app.put("/edit/article/")
async def edit_article(dto: Encrypted_Edit_Article_DTO):

    if not Authenticate_JWT_Claims(dto.token):
        raise HTTPException(status_code=401, detail="Error J")

    try:
        decrypted = {
            "document_id": Decryptor(dto.document_id),
            "user_id": Decryptor(dto.user_id),
            "language": Decryptor(dto.language),
            "region": Decryptor(dto.region),
            "headline": Decryptor(dto.headline),
            "subheadline": Decryptor(dto.sub_headline),
            "byline": Decryptor(dto.byline),
            "image_urls": json.loads(Decryptor(dto.image_urls)) if dto.image_urls else [],
            "body": json.loads(Decryptor(dto.body)) if dto.body else [],
            "tags": json.loads(Decryptor(dto.tags)) if dto.tags else [],
            "source_urls": json.loads(Decryptor(dto.source_urls)) if dto.source_urls else [],
        }

        if not ObjectId.is_valid(decrypted["document_id"]):
            raise HTTPException(status_code=400, detail="Error K")

        article = await Article.get(PydanticObjectId(decrypted["document_id"]))
        if article is None:
            raise HTTPException(status_code=404, detail="Error L")

        article.user_id = decrypted["user_id"]
        article.language = decrypted["language"]
        article.region = decrypted["region"]
        article.headline = decrypted["headline"]
        article.subheadline = decrypted["subheadline"]
        article.byline = decrypted["byline"]
        article.image_urls = decrypted["image_urls"]
        article.body = decrypted["body"]
        article.tags = decrypted["tags"]
        article.source_urls = decrypted["source_urls"]
        article.updated_on = int(datetime.utcnow().timestamp() * 1000)

        await article.save()
        return Encryptor("true")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error M")