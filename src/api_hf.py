import os
import json
from transformers import AutoTokenizer, AutoModel
import uvicorn
from fastapi import FastAPI, Request
import datetime
from model import process_image
import torch
from method import *
from dotenv import load_dotenv

load_dotenv('.env')
cache_dir = os.environ['cache_dir']

tokenizer = AutoTokenizer.from_pretrained("THUDM/visualglm-6b", cache_dir=cache_dir, local_files_only=True, trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/visualglm-6b", device_map='auto', cache_dir=cache_dir, local_files_only=True, trust_remote_code=True).half()

app = FastAPI()
@app.post('/')
async def visual_glm(request: Request):
    json_post_raw = await request.json()
    print("Start to process request")

    json_post = json.dumps(json_post_raw)
    request_data = json.loads(json_post)

    history = request_data.get("history")
    input_image = request_data.get("image")
    query = request_data.get("text")

    if(str(input_image).startswith('http')):
        input_image = await fetch_image_base64(input_image)

    image_path = process_image(input_image)

    with torch.no_grad():
        result = model.stream_chat(tokenizer, image_path, query, history=history)
    last_result = None
    for value in result:
        last_result = value

    answer = last_result[0]
    history = last_result[1]

    history.append((query, answer))
    if os.path.isfile(image_path):
        os.remove(image_path)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    response = {
        "result": answer,
        "history": history,
        "status": 200,
        "time": time
    }
    return response


if __name__ == "__main__":
   uvicorn.run(app, host='0.0.0.0', port=8080, workers=1)