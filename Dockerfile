
# ------------------------------------------------------------------------------
# Base image
# ------------------------------------------------------------------------------
FROM python:3.8-slim AS base

# PIP
# RUN apt-get update 
# RUN  apt-get install -y wget 
# wget
RUN apt-get update && apt-get install -y gnupg2
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive

# CHROME
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable

# CHROME_DRIVER
RUN apt-get install -yqq unzip
RUN apt-get install -y curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

# ------------------------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------------------------
FROM base AS deps
COPY requirements.txt ./
RUN apt update > /dev/null && \
        apt install -y build-essential && \
        pip install --disable-pip-version-check -r requirements.txt

# ------------------------------------------------------------------------------
# Final image
# ------------------------------------------------------------------------------
FROM base
WORKDIR /app
COPY . /app

COPY --from=deps /root/.cache /root/.cache
RUN pip install --disable-pip-version-check -r requirements.txt && \
        rm -rf /root/.cache

EXPOSE 8000

CMD ["gunicorn", "--preload", "-c", "gunicorn.conf.py", "app.main:create_app()"]

