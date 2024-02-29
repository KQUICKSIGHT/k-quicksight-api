# Example using a Debian-based image
FROM python:3.8-slim

# Install git and libpq-dev
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of your application
COPY . .

CMD [ "python3", "manage.py", "runserver", "--settings=k_qicksight_app.settings", "0.0.0.0:8000", "--noreload"]
