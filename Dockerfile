# Start from a base image that includes Python
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install the dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app/

# Expose the port the app runs on (8000 is the default for FastAPI)
EXPOSE 8000

# Command to run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
