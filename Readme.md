# Model Serving Framework

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

## Overview

This code is an attempt to explain in simple language how modern Model Serving frameworks works.

## Features

- **Customizable Model Serving**: Create and deploy machine learning models easily.
- **Integration with scikit-learn**: Out-of-the-box support for scikit-learn models.
- **Docker Integration**: Build and package your models as Docker containers.
- **CLI for Simplified Workflow**: Command-line interface for building and deploying models.

## Components

1. **Framework ServingML**:
   - Contains a base class for creating model instances.
   - Integrates with scikit-learn and other libraries.
   - Provides a `Dockerfile.j2` template for creating Docker containers for specific models.

2. **CLI (Command-Line Interface)**:
   - A tool to compile all necessary code into a single directory.
   - Includes a deploy command that passes the Dockerfile and files to the ServingML server.

3. **ServingML Server**:
   - Receives a directory with a Dockerfile, model, and other code.
   - Creates a Docker image and container for deploying the model.
   - Can run locally or as a remote service for REST API requests.

### Prerequisites

- Python 3.9+
- Docker

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/model-serving-framework.git
   ```
