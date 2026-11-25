from fastapi import FastAPI, HTTPException, Depends
from bson import ObjectId
from app import schemas
from app.database import get_collection

app = FastAPI(title="LR4 — MongoDB")

def valid_oid(id_str: str) -> ObjectId:
    if not ObjectId.is_valid(id_str):
        raise HTTPException(400, "Неверный id")
    return ObjectId(id_str)

@app.post("/students", response_model=schemas.StudentOut, status_code=201)
async def create_student(data: schemas.StudentCreate, col=Depends(get_collection)):
    existing = await col.find_one({"email": data.email})
    if existing:
        raise HTTPException(400, "Студент с таким email уже есть")
    result = await col.insert_one(data.model_dump())
    return {**data.model_dump(), "id": str(result.inserted_id)}

@app.get("/students", response_model=list[schemas.StudentOut])
async def get_students(col=Depends(get_collection)):
    students = []
    async for doc in col.find():
        students.append({**doc, "id": str(doc["_id"])})
    return students

@app.get("/students/{student_id}", response_model=schemas.StudentOut)
async def get_student(student_id: str, col=Depends(get_collection)):
    doc = await col.find_one({"_id": valid_oid(student_id)})
    if not doc:
        raise HTTPException(404, "Студент не найден")
    return {**doc, "id": str(doc["_id"])}

@app.put("/students/{student_id}", response_model=schemas.StudentOut)
async def update_student(student_id: str, data: schemas.StudentUpdate, col=Depends(get_collection)):
    result = await col.update_one(
        {"_id": valid_oid(student_id)},
        {"$set": {"name": data.name}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Студент не найден")
    doc = await col.find_one({"_id": valid_oid(student_id)})
    return {**doc, "id": str(doc["_id"])}

@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: str, col=Depends(get_collection)):
    result = await col.delete_one({"_id": valid_oid(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Студент не найден")
    return None
