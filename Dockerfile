FROM python:3.9.5


WORKDIR /astera-bot


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY ./app ./app


CMD ["python3", "./app/Astera.py"]
