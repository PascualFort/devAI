# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Update packages and install necessary tools
RUN apt-get update && apt-get install -y sudo

# Create a new user and add the user to the sudo group
RUN useradd -m myuser && echo "myuser:myuser" | chpasswd && adduser myuser sudo

# Set the working directory to /app
WORKDIR /app

# Switch back to the myuser
USER myuser

# Copy the requirements.txt file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Run the application
CMD ["python", "-u", "devAI.py"]
