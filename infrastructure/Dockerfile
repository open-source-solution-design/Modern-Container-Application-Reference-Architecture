# Pull a base image
FROM python:3.9

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application:
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

