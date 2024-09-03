# bus-tracker/backend/Dockerfile
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir "fastapi[standard]"

# Copy the backend code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & python check_db.py"]
