FROM python:3.11-bullseye

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY data.csv /app/data.csv

COPY RGHW1.py /app/RGHW1.py

CMD ["python3", "RGHW1.py"]