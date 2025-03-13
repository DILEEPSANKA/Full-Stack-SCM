# Use the official Python runtime as a parent image
FROM python:3.13.1

# Set the working directory inside the container to /app
WORKDIR /kafka/server

# Copy the contents of the current directory into the above mentioned container's workdir.
COPY . /kafka/server

# Run the pip install command inside the container to install the specified Python packages.
RUN pip install confluent-kafka

# Expose port 12345 to allow communication to/from the container.
EXPOSE 12345

# Whenever the container runs, this default command will be executed.
CMD ["python", "server.py"]