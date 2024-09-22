FROM python:3.9-slim AS builder

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone the repository if it doesn't exist; fetch the latest if it does
RUN if [ -d "/app" ]; then \
        cd /app && git fetch origin && git reset --hard origin/main; \
    else \
        git clone https://github.com/frankrodrigo/flaskupload.git /app; \
    fi

# Set the working directory
WORKDIR /app

# Copy the JSON file to the root of the application
COPY cbd3354-435500-07a4e244e7c4.json /app/

# Change the permissions of the JSON file
RUN chmod 644 cbd3354-435500-07a4e244e7c4.json

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the necessary port
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]
