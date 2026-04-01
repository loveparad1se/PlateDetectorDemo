import os
import time
import cv2
import numpy as np
import paddle
from paddleocr import PaddleOCR
from ultralytics import YOLO

model_path = './best.onnx'
model = YOLO(model_path)
ocr = PaddleOCR(use_angle_cls=True, lang='ch', enable_mkldnn=False)

def car_detect(file, save_path='./uploads/', save_crop_path='./crops/'):
    # 检测图片的储存
    now_time = str(int(time.time()))
    filename = now_time + '.jpg'
    
    # 确保目录存在
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_crop_path, exist_ok=True)
    
    with open(save_path + filename, 'wb') as f:
        f.write(file.file.read()) # 将读取的图片写入当前文件
        # file是前端传入的文件对象
        # 读取前端传入的文件内容,将内容写入创建的f里
    results = model.predict(save_path + filename)
    
    # 调用save_crop方法，保存裁剪结果到指定目录
    results[0].save_crop(save_crop_path)
    # save_crop是ultralytics的方法,将检测到的目标裁剪出来，保存到指定路径
    # 这个函数会根据检测到的类别名称，在 save_crop_path 目录下自动创建一个子文件夹（比如名为 license_plate 的文件夹），然后把裁剪出的图片以 im.jpg 这样的通用名称保存在里面。
    # 所以，完整的文件路径就是：[你给的目录] + [自动创建的类别文件夹] + [自动命名的图片]。

        # ========== 修改开始 ==========
    # 动态查找最新的裁剪图片（而不是固定 im.jpg）
    crop_dir = os.path.join(save_crop_path, "license_plate")
    # 拼接路径，后者是yolo自动裁剪后创建的文件夹
    img_crop_path = None  # 先定义为NOne避免报错
    if os.path.exists(crop_dir):
        #检查 license_plate 文件夹是否存在。如果不存在（比如 YOLO 没检测到车牌），跳过查找。
        images = [f for f in os.listdir(crop_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        # os.listdir列出了./crops/license_plate所有图片名
        # 循环所有文件名，且将文件名全部转化为小写，endswith检查是否以括号内内容结尾
        # images是一个列表，存储了所有符合条件的图片
        if images:
            # 按修改时间排序，取最新的
            # 按降序排列所以文件名，最新在最前面
            images.sort(key=lambda x: os.path.getmtime(os.path.join(crop_dir, x)), reverse=True)
            # x是imges列表中的每个元素
            # os.path.join(crop_dir, x)	获取图片完整路径，如 ./crops/license_plate/im.jpg
            # os.path.getmtime()	获取文件的最后修改时间（返回时间戳，如 1743500000.0）
            # key=lambda x: ...	告诉 sort 按哪个值排序，这里按修改时间(告诉sort怎么对images里每张图片排序)
            # 告诉sort按每张图片的修改时间对images列表进行排序(images里存了每张图片的图片名)
            # lambda返回的是每张图片的修改时间(降序排序)
            # reverse=True	降序排列，最新的在最前面
            img_crop_path = os.path.join(crop_dir, images[0])
            # 排序前: ['im.jpg', 'im2.jpg', 'im3.jpg']
            # 排序后: ['im3.jpg', 'im2.jpg', 'im.jpg']
            # 所以这里拼接了最新的图片的完整路径


    # 调用ocr识别裁剪后的车牌
    # 修正路径分隔符兼容Linux
    # img = cv2.imread(img_crop_path)
    result = ocr.ocr(img_crop_path)
    print(f"OCR 原始结果: {result}")
    rec_texts = []
    rec_scores = []
    if result and result[0]:
        rec_texts = result[0].get('rec_texts', []) # get时若不存在'rec_texts'则返回空列表
        rec_scores = result[0].get('rec_scores', [])
        print(f'车牌:{rec_texts[0]}, 置信度:{rec_scores[0]:.2f}')
    
    return {
        'code': 200 if rec_texts else 201,  # 200成功，201未识别到文字
        'msg': '识别完成' if rec_texts else '未识别到车牌文字',
        'data': {
            'plate_text': rec_texts[0] if rec_texts else '',
            'score': rec_scores[0] if rec_scores else 0,
            'filename': filename,
            'origin_path': save_path + filename,
            'crop_path': img_crop_path if rec_texts else ''
        }
    }
