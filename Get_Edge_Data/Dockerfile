FROM python:3.9

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your Selenium test files into the container
COPY . .

# Command to run your Selenium tests
CMD ["python", "./scripts/getPlayerData.py", "&&", "python", "./scripts/getEdgeData.py", "&&", "python", "./scripts/sendData.py"]
