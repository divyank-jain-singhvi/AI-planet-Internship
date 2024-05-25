from fastapi import FastAPI,Depends,HTTPException,UploadFile, File
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import models
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
import fitz
import os
from train_model import model,response
app = FastAPI()

origins=[
    'http://localhost:3000'
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

models.Base.metadata.create_all(bind=engine)

QUESTION=[]
class Question(BaseModel):
    question:str=Field()
    answer: str=Field()

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def read_api(db:Session=Depends(get_db)):
    return db.query(models.Question).all()

@app.post("/")
def create_question(question:Question,db:Session=Depends(get_db)):
    question_model=models.Question()
    question_model.question=question.question
    # question_model.answer=question.answer
    data=response(question.question)
    question_model.answer=data['answer']
    # print(question,question.question,question.answer)
    db.add(question_model)
    db.commit()
    
    # print(data['answer'])
    
    return question

@app.post('/uploadfile')
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "D:/Full stack pdf analyze project/backend/uploaded file/"
    os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
    # Concatenate the directory path with the file name to get the full path
    file_path = os.path.join(upload_dir, file.filename)
    
    # Open the file in write-binary mode and save the contents
    with open(file_path, "wb") as f:
        f.write(await file.read())
    model(file.filename)
    
    return {"filename": file.filename,"answer":'your model is ready for answers'}
