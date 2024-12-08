 MLOps Pipeline for Advanced Workflows

Overview

This project implements a scalable and extendable MLOps pipeline integrating MLFlow for model versioning, Airflow for workflow automation, and CI/CD pipelines for deploying a full-stack application. The goal is to simplify managing the ML lifecycle, from experimentation to deployment, using modern tools like Docker and Kubernetes.

Features

MLFlow for model experiment tracking and versioning.

Apache Airflow for automated workflow scheduling.

CI/CD Pipelines for streamlined integration and deployment.

Docker for consistent runtime environments.

Kubernetes for container orchestration and scaling.

Architecture

The architecture includes:

Model Training and Versioning: Handled by MLFlow.
Workflow Automation: Managed by Airflow DAGs.
Containerization and Deployment: Using Docker and Kubernetes.
Continuous Integration/Deployment: Powered by GitHub Actions.

Installation

Prerequisites
Ensure the following tools are installed:

Python (3.8 or higher)

Docker and Docker Compose

Kubernetes (Minikube or a similar platform)

Git

MLFlow and Apache Airflow

Pipeline Execution

Experiment Tracking:
Open MLFlow UI at http://127.0.0.1:5000.
View logged parameters, metrics, and artifacts.
Workflow Automation:

Access the Airflow web UI at http://127.0.0.1:8080.
Monitor DAG execution and logs.
CI/CD Workflow:

Push changes to the dev branch for CI tests.
Merge pull requests to testing for pre-deployment checks.
Merge to prod for production deployment.

