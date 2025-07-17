from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4

app = FastAPI()

class Post(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    content: str
    date: datetime = datetime.now()


posts = []
@app.get("/")
def home():
    return {"welcome":"API WELCOME"}

@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts")
def save_post(post: Post):
    if post.id == None:
        post.id = str(uuid4())
    posts.append(post.model_dump())
    return post.model_dump()

@app.get("/posts/{id_}")
def get_post(id_:str):
    for post in posts:
        if post["id"] == id_:
            return post
    raise HTTPException(status_code=404,detail="Not found")

@app.delete("/posts/{id}")
def delete_post(id:str):
    for post in range(len(posts)):
        if posts[post]["id"] == id:
            aux = posts[post]
            posts.pop(post)
            return {"Post deleted":aux}
    raise HTTPException(status_code=404,detail="Not found")
        
@app.put("/posts")
def update_post(new_post:Post):
    for index in range(len(posts)):
        if posts[index]["id"] == new_post.id:
            posts[index]["title"] = new_post.title
            posts[index]["author"] = new_post.author
            posts[index]["contente"] = new_post.content
            return {"Post updated": new_post}
    raise HTTPException(status_code=404,detail="Not found")