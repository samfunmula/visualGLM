FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src .
COPY modeling_chatglm.py /root/.cache/huggingface/modules/transformers_modules/THUDM/visualglm-6b/f4f759acde0926fefcd35e2c626e08adb452eff8/modeling_chatglm.py
EXPOSE 8080

CMD uvicorn api_hf:app --workers 1 --host 0.0.0.0 --port 8080 --timeout-keep-alive 30