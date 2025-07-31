FROM python:3.13-slim

WORKDIR /app


COPY ./requirements.txt /app/requirements.txt
RUN pip install --root-user-action=ignore --no-cache-dir -r ./requirements.txt


COPY . /app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]