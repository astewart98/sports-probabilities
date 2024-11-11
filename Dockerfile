# Use a Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the contents of your local folder to /app in the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
