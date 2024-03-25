from fastapi import FastAPI
from pr1.endpoints import router
import uvicorn


app = FastAPI()
#из доклада
# app = FastAPI(
#     title="Related Blog Articles",
#     description="This API was built with FastAPI and exists to find related profiles.",
#     version="1.0.0",
# )

# app = FastAPI(
#     title="Related Blog Profiles",
#     description="This API was built with FastAPI and exists to find related profiles.",
#     version="1.0.0",
#     servers=[
#         {
#             "url": "http://localhost:8000",
#             "description": "Development Server"
#         },
#         {
#             "url": "https://mock.pstmn.io",
#             "description": "Mock Server",
#         }
#     ],
# )

# ####ПРИМЕР 2####
#
# app = FastAPI(
#     title="ProfileApp",
#     description="description",
#     summary="Summary of application",
#     version="0.0.1",
#     terms_of_service="http://example.com/terms/",
#     contact={
#         "name": "Maria",
#         "url": "http://x-force.example.com/contact/",
#         "email": "maria@itmo.example.com",
#     },
#     license_info={
#         "name": "Apache 2.0",
#         "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
#     },
# )

# ####ПРИМЕР 3
# from fastapi import FastAPI
#
# tags_metadata = [
#     {
#         "name": "users",
#         "description": "Operations with users. The **login** logic is also here.",
#     },
#     {
#         "name": "items",
#         "description": "Manage items. So _fancy_ they have their own docs.",
#         "externalDocs": {
#             "description": "Items external docs",
#             "url": "https://fastapi.tiangolo.com/",
#         },
#     },
# ]
#
# app = FastAPI(openapi_tags=tags_metadata)
#
#
# @app.get("/users/", tags=["users"])
# async def get_users():
#     return [{"name": "user2"}, {"name": "user3"}]
#
#
# @app.get("/items/", tags=["items"])
# async def get_items():
#     return [{"name": "item1"}, {"name": "item2"}]
#
# @app.get("/items/")
# async def read_items():
#     return [{"name": "Katana"}]
app.include_router(router)

@app.get("/")
def hello():
    return "Hello, Maria!"

# @app.get("/s", name="Index", summary="Returns the name of the API", tags=["Routes"])
# def hello():
#     return "Hello, Maria!"
# @app.get(
#     "/article/related",
#     summary="Finds related article IDs.",
#     description="Generates a kNN model from all the articles on the blog.\
#         The clusters are based on categories, sub-categories, and tags.\n After the clusters are created,\
#             three IDs are selected from the cluster that the submitted ID belongs to.",
#     response_description="List of article IDs.",
#     responses={
#         200: {
#             "content": {
#                 "application/json": {
#                     "example": {
#                         "ids": [
#                             "96caaf28-48d2-4a9a-8a3f-9e96ca333e90",
#                             "19be8556-7742-41a3-b22d-5cf4676674f4",
#                             "da7d5941-a78f-44a8-b63b-18b460640c92",
#                         ]
#                     }
#                 }
#             },
#         },
#         404: {
#             "description": "Article ID not found in model.",
#             "content": {
#                 "application/json": {
#                     "example": {"message": "Article ID not found in DataFrame"}
#                 }
#             },
#         },
#     },
#     tags=["Routes"],
# )
#
# def hello():
#     return "Hello, Maria!"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)