FROM ubuntu:latest

# Install any dependencies needed for your commands
RUN apt-get update && \
    apt-get install -y \
    bash

# Set a working directory
WORKDIR /app/temp

# Copy your command runner script into the container
COPY runner.sh /app/temp

# Set permissions if necessary
RUN chmod +x /app/temp/runner.sh

# Define the default command to run when the container starts
CMD ["/app/temp/runner.sh"]
