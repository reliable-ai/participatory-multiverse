FROM python:3.13-slim

# Set meta information
LABEL org.opencontainers.image.source="https://github.com/reliable-ai/participatory-multiverse-simulation"
LABEL org.opencontainers.image.description="New container image to run the multiverse analysis described in 'Preventing Harmful Data Practices by using Participatory Input to Navigate the Machine Learning Multiverse'."
LABEL org.opencontainers.image.licenses="CC BY 4.0"

# Install dependencies for python packages
RUN apt-get update && \
    apt-get install -y gcc git  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install uv
RUN pip install uv

# Install package
RUN uv sync

# Define environment variable
ENV SEED=2024
ENV MODE="full"

CMD ["sh", "-c", "uv run -m multiversum --mode $MODE --seed $SEED"]
