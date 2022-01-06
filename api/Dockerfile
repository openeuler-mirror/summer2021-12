FROM python:3.8
WORKDIR /faq/api

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 8080

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]

