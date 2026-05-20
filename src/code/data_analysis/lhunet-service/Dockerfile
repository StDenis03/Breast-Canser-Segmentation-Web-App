FROM python:3.12-slim

WORKDIR /opt/service

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    git \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/service/requirements.txt
RUN pip install --no-cache-dir -r /opt/service/requirements.txt

COPY app /opt/service/app
COPY docker/entrypoint.sh /opt/service/docker/entrypoint.sh
COPY LHUNet /opt/LHUNet
COPY models /opt/service/models

ENV HOST=0.0.0.0
ENV PORT=8000
ENV MODEL_DIR=/opt/service/models/lhunet_breastct
ENV nnUNet_extTrainer=/opt/LHUNet/src

EXPOSE 8000

ENTRYPOINT ["/opt/service/docker/entrypoint.sh"]
