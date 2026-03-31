import os
import sqlite3
from datetime import datetime
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from carplatedetct import car_detect 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for d in ["uploads", "crops"]:
    if not os.path.exists(d): os.makedirs(d)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS car 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, origin_img TEXT, plate_text TEXT, username TEXT, create_time TEXT)''')
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/api/detect")
async def detect_api(file: UploadFile = File(...), username: str = Form("管理员")):
    result = car_detect(file)
    if result.get("code") == 200:
        data = result.get("data")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO car (origin_img, plate_text, username, create_time) VALUES (?, ?, ?, ?)",
            (data.get("origin_path"), data.get("plate_text"), username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    return result

# ========== 添加不带 /api 的路由（兼容前端） ==========

@app.post("/detect")
async def detect_api_alias(file: UploadFile = File(...), username: str = Form("管理员")):
    return await detect_api(file, username)

@app.get("/history")
async def get_history(keyword: str = None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if keyword:
        cursor.execute("SELECT * FROM car WHERE plate_text LIKE ? ORDER BY id DESC", (f'%{keyword}%',))
    else:
        cursor.execute("SELECT * FROM car ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "origin_img": r[1], "plate_text": r[2], "username": r[3], "create_time": r[4]} for r in rows]

@app.delete("/history/{record_id}")
async def delete_history(record_id: int):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM car WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return {"success": True}

# ========== 添加根路径（可选） ==========

@app.get("/")
async def root():
    return {"message": "车牌检测系统 API", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


