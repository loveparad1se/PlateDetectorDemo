# 车牌检测识别系统

基于 YOLO + PaddleOCR 的车牌检测与识别系统。

## 功能特点

- 上传图片，自动检测车牌位置
- 使用 PaddleOCR 识别车牌号码
- 历史记录查询与管理
- 语音播报识别结果

## 技术栈

- 后端：FastAPI + SQLite
- 前端：Vue.js + Element UI
- 模型：YOLO + PaddleOCR

## 安装与运行

### 后端

cd backend
pip install -r requirements.txt
python main.py


### 前端

cd frontend
npm install(非必要)
npm run serve

### 访问地址

前端：http://localhost:8080
后端 API：http://localhost:8000/docs