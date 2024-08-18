FROM python:slim

WORKDIR /app
COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY . .
CMD ["fastapi", "run", "transit34_fastapi/src/transit34_fastapi/__init__.py"]
