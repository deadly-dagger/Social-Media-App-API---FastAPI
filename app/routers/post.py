from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix ="/posts",
    tags = ['Posts']
)


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() ------- For just returning posts
            # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() for posts by own user. Notes app can use this
            # Add post.owner_id != current_user.id to avoid unauthorized access for private apps like notes.
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).all()

    
    return results
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # return {"data": posts}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published)) # Formatting prevents SQL injection
    # new_post = cursor.fetchone()

    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Instead of returning *
    return new_post






# For getting one specfic post:- 
# below line, 'id: int' checks type compatibility and converts into int, we do this so that random strings are not sent as id. Eg. abcd
# def get_post(id: int, response: Response): use response if needed
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,
    #                str(id))  # We convert int back to string
    # post = cursor.fetchone()

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute( """ DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authroized to perform action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
   
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authroized to perform action")

    post_query.update(updated_post.dict(), synchronize_session=False) 
    db.commit()
    return post_query.first()



'''
Used before Database to check CRUD points, checked with a dummy array in memory

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


Creating a post
post_dict = post.dict()
post_dict['id'] = randrange(0, 1000000000)
my_posts.append(post_dict)
return {"data": post_dict}


 For finding a specifc post
    post = find_post(id)
        # alternative for exception:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} not found"}
    return {"post_details": post}
'''