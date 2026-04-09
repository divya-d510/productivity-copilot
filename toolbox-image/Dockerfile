FROM debian:12-slim

WORKDIR /app

# Detect architecture and download appropriate toolbox binary
RUN apt-get update && apt-get install -y curl ca-certificates && \
    ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ]; then \
      curl -L -o /usr/local/bin/toolbox \
        https://storage.googleapis.com/genai-toolbox/v0.31.0/linux/arm64/toolbox; \
    else \
      curl -L -o /usr/local/bin/toolbox \
        https://storage.googleapis.com/genai-toolbox/v0.31.0/linux/amd64/toolbox; \
    fi && \
    chmod +x /usr/local/bin/toolbox && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY tools.yaml /app/tools.yaml

EXPOSE 8080

CMD ["/usr/local/bin/toolbox", "--config", "/app/tools.yaml", "--address", "0.0.0.0", "--port", "8080"]
