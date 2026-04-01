import os
import sqlite3
import uvicorn
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 确保你的项目中有这个文件
from carplatedetct import car_detect 

# --- 1. 数据库初始化逻辑 ---
DB_PATH = 'database.db'

def init_db():
    """初始化数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 显式定义表结构，确保字段顺序固定
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            origin_img TEXT, 
            plate_text TEXT, 
            username TEXT, 
            create_time TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("数据库初始化成功或已存在。")

# --- 2. 使用最新的 Lifespan 管理生命周期 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 程序启动时执行
    init_db()
    yield
    # 程序关闭时执行（如需清理资源可写在这里）
    print("正在关闭服务器...")

# --- 3. 创建 FastAPI 实例 ---
app = FastAPI(lifespan=lifespan)

# 配置跨域 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保必要的目录存在
for d in ["uploads", "crops"]:
    if not os.path.exists(d): 
        os.makedirs(d)

# 挂载静态文件目录，方便前端通过 URL 访问图片
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/crops", StaticFiles(directory="crops"), name="crops")

# --- 4. 路由定义 ---

@app.post("/api/detect")
@app.post("/detect")  # 兼容前端不同的请求路径
async def detect_api(file: UploadFile = File(...), username: str = Form("管理员")):
    """车牌检测与识别接口"""
    # 调用识别算法
    result = car_detect(file)
    
    if result.get("code") == 200:
        data = result.get("data")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            # 严格按照 (origin_img, plate_text, username, create_time) 顺序插入
            cursor.execute(
                "INSERT INTO car (origin_img, plate_text, username, create_time) VALUES (?, ?, ?, ?)",
                (
                    data.get("origin_path"), 
                    data.get("plate_text"), 
                    username, 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"数据库入库报错: {e}")
            
    return result

@app.get("/history")
async def get_history(keyword: str = None):
    """获取识别历史记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 关键修正：显式查询字段，防止 SELECT * 导致的列错位
    base_sql = "SELECT id, origin_img, plate_text, username, create_time FROM car"
    
    if keyword:
        # 支持按车牌号模糊搜索
        cursor.execute(base_sql + " WHERE plate_text LIKE ? ORDER BY id DESC", (f'%{keyword}%',))
    else:
        cursor.execute(base_sql + " ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    
    # 将元组转换为前端易读的字典对象
    # 索引对应：0:id, 1:img, 2:plate, 3:user, 4:time
    return [
        {
            "id": r[0], 
            "origin_img": r[1], 
            "plate_text": r[2], 
            "username": r[3], 
            "create_time": r[4]
        } for r in rows
    ]

@app.delete("/history/{record_id}")
async def delete_history(record_id: int):
    """根据 ID 删除记录"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM car WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        return {"success": True, "msg": "删除成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}

@app.get("/")
async def root():
    return {"status": "running", "version": "2.0"}

# --- 5. 启动入口 ---
if __name__ == "__main__":
    # 如果 8000 还是报端口占用，请手动将下面的 8000 改为 8001
    uvicorn.run(app, host="0.0.0.0", port=8000)




