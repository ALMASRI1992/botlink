# Use an official Python image
FROM python:3.12-slim

# Install dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    && apt-get install -y \
    libx11-dev \
    libxcomposite-dev \
    libxrandr-dev \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libnss3 \
    libxss1 \
    libgconf-2-4 \
    libasound2 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libnspr4 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    lsb-release \
    xdg-utils \
    libgbm1 \
    libvulkan1 \
    --no-install-recommends

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get install -f -y
# Install WebDriver Manager
RUN pip install selenium webdriver-manager

# Set working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY backend/requirements.txt /app/requirements.txt
# Copy all necessary files
#COPY . .
COPY backend/ /app/
# Install Python dependencies
RUN python -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r /app/requirements.txt
# Expose the necessary port
EXPOSE 8080
# Run the Flask app
CMD [".venv/bin/python", "/app/app.py"]

RUN google-chrome-stable --version

