FROM python:3.9

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip && \
    apt-get install -y chromium

# Download and install Google Chrome
RUN wget -q -O /tmp/chrome-linux64.zip "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chrome-linux64.zip" && \
    unzip /tmp/chrome-linux64.zip -d /usr/bin && \
    rm /tmp/chrome-linux64.zip && \
    chmod +x /usr/bin/chrome-linux64/chrome

# Download and install ChromeDriver
RUN wget -q -O /tmp/chromedriver-linux64.zip "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /usr/bin && \
    rm /tmp/chromedriver-linux64.zip && \
    chmod +x /usr/bin/chromedriver-linux64/chromedriver

# Set symbolic link for ChromeDriver
RUN ln -s /usr/bin/chromedriver-linux64/chromedriver /usr/bin/chromedriver

# install selenium

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your Selenium test files into the container
COPY . .

# Copy the script file and make it executable
COPY run_scripts.sh .
RUN chmod +x run_scripts.sh

# Command to run the script
CMD ["./run_scripts.sh"]
