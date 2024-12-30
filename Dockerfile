# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the container
COPY . .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Set the command to run the Flask app
CMD ["python", "app.py"]
