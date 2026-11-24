from pydantic import BaseModel, Field, EmailStr

class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

class StudentUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class StudentOut(StudentCreate):
    id: str  # MongoDB использует ObjectId, сериализуем как строку