FROM python:3.12.4-slim AS ubuntu

# Install required packages
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN apt-get install -y ffmpeg git curl

# Copy requirements file
COPY ./requirements.txt /app/

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy application files
COPY . .

RUN python3 manage.py migrate

# Ensure manage.py exists in /app
RUN if [ ! -f "/app/manage.py" ]; then echo "Error: manage.py not found"; exit 1; fi

# Set the entry point
ENTRYPOINT ["python3", "manage.py", "runserver"]
