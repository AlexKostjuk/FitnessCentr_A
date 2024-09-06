FROM python:3.9-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
#COPY gunicorn_app /app

EXPOSE 8080

#CMD ["python", "app_test.py"]