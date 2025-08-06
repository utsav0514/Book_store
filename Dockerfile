FROM python:3.11-slim as builder
WORKDIR /app

COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

FROM python:3.11-slim 
WORKDIR /app

COPY --from=builder /usr/local  /usr/local

COPY . .
EXPOSE 8000

CMD ["python", "Hello/manage.py", "runserver", "0.0.0.0:8000"]

