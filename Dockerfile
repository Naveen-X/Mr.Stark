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
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get install -y --no-install-recommends \
    mediainfo \
    ffmpeg \
    gifsicle \
    libgl1-mesa-glx && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable --no-install-recommends && \
    CHROMEDRIVER_VERSION=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$(google-chrome-stable --version | awk '{print $3}' | awk -F. '{print $1}')) && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver && \
    rm /tmp/chromedriver.zip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# RUN mkdir -p /app/resources/ai_helpers && \
#     wget https://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel -P /app/resources/ai_helpers/

#uv -p python3.11 pip ...`
RUN uv pip install --system --no-cache -r req.txt
RUN uv pip install --system --no-cache -r requirements.txt

CMD ["python3.11", "-m", "Stark"]
