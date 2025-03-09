# FastAPI-AWS-Boilerplate
it's a starter project for FastAPI &amp; AWS

project_root/
│── app/
│   ├── main.py  # FastAPI application
│   ├── database.py  # SQLAlchemy setup with PostgreSQL
│   ├── models.py  # Database models
│   ├── schemas.py  # Pydantic schemas
│   ├── crud.py  # Database operations
│   ├── dependencies.py  # Dependency injection (DB session, etc.)
│   ├── routers/
│   │   ├── data.py  # API routes
│
│── tests/
│   ├── test_main.py  # Unit tests for API endpoints
│
│── docker/
│   ├── Dockerfile  # Container for FastAPI app
│   ├── docker-compose.yml  # Setup for PostgreSQL & API locally
│
│── deploy/
│   ├── serverless.yml  # AWS Lambda deployment config
│   ├── requirements.txt  # Dependencies
│
│── .github/
│   ├── workflows/
│   │   ├── ci-cd.yml  # GitHub Actions for CI/CD pipeline
│
│── Jenkinsfile  # Alternative CI/CD with Jenkins
│── README.md  # Project breakdown and setup instructions

# README.md

# Python API with SQL, AWS, and CI/CD

## Project Overview
This project is a minimal FastAPI-based REST API that:
- Uses **PostgreSQL** as a database (SQL experience)
- Runs inside a **Docker container** (Docker/Kubernetes experience)
- Deploys to **AWS Lambda** using the **Serverless Framework**
- Uses **GitHub Actions (or Jenkins)** to automate deployment

## Tech Stack
- **Python** (FastAPI, SQLAlchemy, Pydantic)
- **PostgreSQL** (Database, via SQLAlchemy)
- **AWS Lambda + RDS** (Cloud deployment)
- **Docker** (Containerization)
- **Jenkins / GitHub Actions** (CI/CD pipeline)

## Features
- `POST /data`: Store data in PostgreSQL
- `GET /data`: Retrieve stored data
- CI/CD: Automated testing, Docker image build, and AWS deployment
