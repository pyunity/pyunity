FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    xvfb \
    libglfw3 \
    python3-opengl \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir glfw -r requirements.txt

COPY pyunity/ ./pyunity

ENV DISPLAY=:5
CMD ["bash", "-c", "xvfb-run -s \"-screen 0, 1366x768x24\" Xvfb :5 & python -m pyunity"]