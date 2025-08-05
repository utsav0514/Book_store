FROM python:3.11-slim
WORKDIR /app

COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 8000

CMD ["python", "Hello/manage.py", "runserver", "0.0.0.0:8000"]

