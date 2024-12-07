# Use a base Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

RUN pip install bcrypt

# Copy dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
