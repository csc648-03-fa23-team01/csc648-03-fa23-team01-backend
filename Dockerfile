# 
FROM python:3.9

# 
COPY . /app

# Set the working directory
WORKDIR /app

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
