# Use the official Python image from Docker Hub
FROM python:3.11

# Set environment variables
ENV CLOUD_SQL_USERNAME=root
ENV CLOUD_SQL_PASSWORD=DBapi@2023
ENV CLOUD_SQL_DATABASE_NAME=apirest
ENV CLOUD_SQL_CONNECTION_NAME=api-rest-401320:southamerica-west1:plapi2023

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port on which your app will run
EXPOSE 8080

# Define the command to run your application
CMD ["python", "apirest.py"]
