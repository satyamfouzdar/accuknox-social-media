# Pull the base image
FROM python:3.9-slim-bullseye

# Set Environment Variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the Workdir
WORKDIR /code

# Install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the project
COPY . .