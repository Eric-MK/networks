# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY load_balancer/requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Just try to copy the load_balancer directory entirely for simplicity
COPY load_balancer /app/

# Try to copy the myserver directory entirely
COPY myserver /app/myserver

# List files in /app to debug
RUN ls -al /app
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Command to run the application
CMD ["python", "load_balancer.py"]
