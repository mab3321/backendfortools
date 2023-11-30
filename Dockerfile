# Use the official Python image
FROM python:3.9

# Set environment variables
ENV PORT=8000
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/google_cred.json

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the specified port
EXPOSE $PORT

# Command to run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app","--timeout","600"]
