FROM python:3.8.18-slim-bookworm

# Set meta information
LABEL org.opencontainers.image.source="https://github.com/reliable-ai/participatory-multiverse-simulation"
LABEL org.opencontainers.image.description="Original container image to run the multiverse analysis in 'Preventing Harmful Data Practices by using Participatory Input to Navigate the Machine Learning Multiverse'."
LABEL org.opencontainers.image.licenses="CC BY 4.0"

# Install dependencies for python packages
RUN apt-get update && \
    apt-get install -y gcc git  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in Pipfile
RUN pip install pipenv
RUN pipenv sync -d

# Define environment variable
ENV SEED 2024
ENV MODE "full"

# Run multiverse_analysis.py when the container launches, passing the seed as an argument
CMD ["pipenv", "run", "python", "multiverse_analysis.py", "--mode", "$MODE", "--seed", "$SEED"]
