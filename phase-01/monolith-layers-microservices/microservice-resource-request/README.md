# Resource Provisioning System

A proof-of-concept demonstrating an asynchronous microservices architecture using FastAPI and RabbitMQ.

## Objective

Receive infrastructure provisioning requests asynchronously.

## Architecture

Request Service

↓

RabbitMQ

↓

Provision Service

↓

RabbitMQ

↓

Notification Service

## Stack

- FastAPI
- RabbitMQ
- SQLite
- Docker Compose

## Project Structure

service-request

service-provision

service-notification

docs

common

## Running

docker compose up --build