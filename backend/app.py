import pandas as pd
import uvicorn
import logging
import os
import csv
from typing import List

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from backend.api.api_insert_update_data import insert_data
from backend.api.api_retrain_model import re_train_model
from backend.api.api_message import send_message
from backend.config.config import Config

app = FastAPI()
templates =  Jinja2Templates(directory = 'templates')

logging.basicConfig(filename=Config.logging,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.post('/api/send-message')
async def api_send_message(request: Request):
    json_param = await request.form()
    json_param = jsonable_encoder(json_param)
    result = send_message(json_param)
    return result


@app.post('/api/send-image')
async def api_send_image(request: Request):
    ''' json_param = await request.form()
    json_param = jsonable_encoder(json_param)
    result = send_image(json_param) '''
    result = {
        'rep_intent': 'inform',
        'suggest_reply': 'Hiện tại chatbot chưa hỗ trợ tính năng gửi ảnh, tính năng này sẽ có trong thời gian sớm nhất ạ.',
        'id_job': 456363,
        'check_end':False
    }
    return result


@app.get('/')
def home():
    return "Covid-chatbot " + str(Config.database["chatbot_conversations"].count_documents({}))


# @app.get('/api/update_database_knn')
# def update_db():
#     data = {
#         'question': ['tôi nên sử dụng xà phòng nào để rửa tay'],
#         'answer': ['iệc sử dụng xà phòng diệt khuẩn RỬA TAY tốt hơn xà phòng thường trong làm giảm nguy cơ gây bệnh tiêu chảy và nhiễm trùng đường hô hấp.']
#     }
#     return insert_update_database(data)


@app.get('/api/export_new_data')
def export_data():
    # mydb = models.myclient["chatbot_data"]
    # mycol = mydb["chatbot_conversations"]
    cursor = Config.database["chatbot_conversations"].find({})
    data = []
    for doc in cursor:
        if 'intent' in doc:
            intent = doc['intent']
        else:
            intent = ''
        
        if 'sub_intent' in doc:
            sub = doc['sub_intent']
        else:
            sub = ''
        data.append({'text': doc['message_text'], 'intent': intent, 'sub_intent': sub})
    
    with open('data_export.csv', encoding='utf-8-sig', mode='w',newline='') as csv_file:
        fieldnames = ['text','intent','sub_intent']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
        
    return FileResponse(path=os.getcwd() + '/data_export.csv', filename='data_export.csv', media_type='text/mp4')


@app.get('/api/re_train_model')
def retrain():
    re_train_model()
    return 'Done'


@app.post("/data/insert")
async def submit_insert(password: str = Form(...), files: List[UploadFile] = File(...)):
    
    data = []
    if password != Config.chatbot_password:
        return 'SAI MAT KHAU'
    for file in files:
        data = await file.read()
        if not data:
            return 'Vui lòng chọn file data'
        try:
            data = pd.read_excel(data)
            data_insert = {
                'text': [ele if pd.notna(ele) else 'None' for ele in data['text'].values],
                'intent': [ele if pd.notna(ele) else 'None' for ele in data['intent'].values],
                'sub_intent': [ele if pd.notna(ele) else 'None' for ele in data['sub_intent'].values],
                'response': [ele if pd.notna(ele) else 'None' for ele in data['response']]
            }
            
            insert_data(data_insert)
        except:
            return "Vui lòng insert data theo đúng format"

    return "Đã insert thành công " +  " và ".join([file.filename for file in files])


@app.get('/api/insert_data')
def insert(request: Request):
    return templates.TemplateResponse("insert.html", {"request": request})


uvicorn.run(app, host=Config.service_host, port=int(Config.service_port))