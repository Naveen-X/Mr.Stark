FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Kolkata
ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    curl \
    wget \
    ca-certificates \
    gnupg \
    unzip \
    tzdata && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-venv && \
    # Install uv
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    mediainfo \
    ffmpeg \
    gifsicle \
    libgl1-mesa-glx \
    dbus-user-session

# Update package index and install base packages
RUN apt-get update
RUN apt-get install -y --no-install-recommends wget gnupg ca-certificates

# Add Google Chrome GPG key and repo
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Update again and install Google Chrome with dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends google-chrome-stable fonts-liberation libu2f-udev xvfb

# Download matching ChromeDriver version
RUN wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver

RUN curl -LsSf https://astral.sh/uv/install.sh | sh 

WORKDIR /app

COPY . .

# RUN mkdir -p /app/resources/ai_helpers && \
#     wget https://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel -P /app/resources/ai_helpers/

#uv -p python3.11 pip ...`
RUN /root/.local/bin/uv pip install --system --no-cache -r req.txt
RUN /root/.local/bin/uv pip install --system --no-cache -r requirements.txt


COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python3.11", "-m", "Stark"]