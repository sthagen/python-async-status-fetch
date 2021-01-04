FROM python:3.9-slim-buster
RUN export DEBIAN_FRONTEND=noninteractive && \
apt-get update && \
apt-get -y upgrade && \
apt-get install -y --no-install-recommends tini && \
apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import compileall; compileall.compile_path(maxlevels=10)"
RUN useradd --create-home action
USER action
WORKDIR /app
COPY app .
RUN python -m compileall app/thing
ENV PYTHONFAULTHANDLER=1
ENTRYPOINT ["tini", "--", "python", "-m", "thing"]
