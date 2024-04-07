# Base image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /django

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project files
COPY . .

CMD python manage.py runserver 0.0.0.0:8000
