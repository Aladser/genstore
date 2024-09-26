FROM python:3.12-slim
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN cat requirements.txt
COPY . .
CMD ["sh", "-c", "python manage.py migrate --seed && python manage.py runserver"]


