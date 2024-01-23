# MQTT Subscriber Application

## Description

This application subscribes to an MQTT topic, logs the received messages, and sends them to a Postgres database. It also provides a REST endpoint using FastAPI to retrieve all these messages. The application is containerized using Docker.

## Installation

To install the application, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`

## Usage

To run the application, follow these steps:

1. Build the Docker image: `docker-compose up --build`
2. The fastapi application will be available at `http://localhost:8000`

## API

The application provides the following REST endpoint:

- `GET /messages`: Retrieves all messages from the database.
