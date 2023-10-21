# Use the official Python image from the Docker Hub
FROM python:3.9

# Copy the local directory's contents to the Docker image
COPY . /app

# Set the working directory in the Docker image
WORKDIR /app

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the wait-for-it.sh script into the Docker image
COPY wait-for-it.sh /wait-for-it.sh

# Make the wait-for-it.sh script executable
RUN chmod +x /wait-for-it.sh

# Start the application
CMD ["/wait-for-it.sh", "db:3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]