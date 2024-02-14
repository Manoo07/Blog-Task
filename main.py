from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class Blog(BaseModel):
    title: str
    content: str

# In-memory database
blogs_db: Dict[int, Blog] = {}

blog_counter = 0

@app.post("/blogs/", response_model=Blog)
def create_blog(blog: Blog):
    # count = count + 1
    global blog_counter
    blog_counter +=1
    blogs_db[blog_counter] = blog
    return blog

@app.get("/blogs/{blog_id}", response_model=Blog)
def read_blog(blog_id: int):
    blog = blogs_db.get(blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.get("/blogs/", response_model=dict)
def read_all_blogs():
    return blogs_db

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, updated_blog: Blog):
    if blog_id not in blogs_db:
        raise HTTPException(status_code=404, detail="Blog not found")
    blogs_db[blog_id] = updated_blog
    return updated_blog

@app.delete("/blogs/{blog_id}", response_model=Blog)
def delete_blog(blog_id: int):
    if blog_id not in blogs_db:
        raise HTTPException(status_code=404, detail="Blog not found")
    deleted_blog = blogs_db.pop(blog_id)
    return deleted_blog
