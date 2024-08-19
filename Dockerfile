FROM python:slim

WORKDIR /app
# Copy is here because the dependencies include packages in the workspace
COPY . . 
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock
CMD ["fastapi", "run", "transit34_fastapi/src/transit34_fastapi/__init__.py"]
