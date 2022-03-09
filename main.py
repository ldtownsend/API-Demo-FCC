from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# @app.post("/posts")
# def create_posts(post: Post): 
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 1_000_000) #for dev only, lazy way of making id
#     my_posts.append(post_dict)
#     return {'data': post_dict}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1_000_000) #for dev only, lazy way of making id
    my_posts.append(post_dict)
    return {'data': post_dict}

# @app.get("/posts/{id}") #id is a path parameter
# def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post with id: {id} was not found."}
#     print(post)
#     return {"post_detail": post}


@app.get("/posts/{id}") #id is a path parameter
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found.")
    return {"post_detail": post}
