# Weather Application

## Introduction

This project is an example of deploying a web-based application on an AWS EKS's cluster, automatically, using a Jenkins CI/CD pipeline. The web-based application provides weather forecasts for various cities using the OpenWeatherMap API to retrieve weather data, and displays the forecast of the requested city/country for the next 7 days. The application is built using Python, Flask and Kubernetes, allowing for scalability and easy deployment.

## Installation and Usage

### Prerequisites

Before running the Weather Application, ensure that the following dependencies are installed on the main server:

- Python (version 3.6 or higher)
- Flask (install via `pip install flask`)
- Docker (for building and pushing container images)
- Kubernetes (for deployment)
- eksctl (for AWS EKS cluster setup)
- AWS account with access to Elastic Container Registry (ECR)

### Setup

1. Clone the repository to your local machine using 'git clone' command.
2. Navigate to the repository's directory.
3. Configure the necessary API keys:
	- OpenWeatherMap: Sign up at [https://openweathermap.org/](https://openweathermap.org/) and obtain an API key.
	- Update the `app_id` and `app_key` variables in the `application.py` file with your API credentials.
4. Set up an EKS cluster using `eksctl create cluster` command and provide your cluster's configuration.
5. Update the `Ingress.yaml` file with the load balancer's DNS associated with your EKS cluster. Replace `[enter-elb-dns]` with the actual DNS value.
6. Create a text file containing your EKS cluster's configuration (from `.kube/config`). This file will be used by Jenkins for deployment. Ensure it is accessible by Jenkins as a secret text named `K8S`.
7. Set up a Jenkins pipeline using the provided `Jenkinsfile`.
8. Inside the Jenkinsfile replace the docker tag and docker registry with your registry's information.
9. Verify that the deployment is running with `kubectl get deployment`, `kubectl get pods`, `kubectl get service` and `kubectl get ingress`.
10. Access the deployed Weather Application using the provided URL or hostname associated with the ingress controller.

## Files

This repository contains the following files:

### Jenkinsfile
Jenkins pipeline script for automating the CI/CD process. It uses a secret file for connecting and deploying on the EKS cluster.

### application.py
Python script for the weather application. It retrieves weather data for the next 7 days using the OpenWeatherMap API. The retrieved data is formatted as a JSON structure and served as a response to incoming requests.

### Dockerfile
For building a docker image. 

### requirements.txt
Contains necessary files for the python application to work properly.

### template html files
The web pages presented to the user.

### Deployment.yaml
Kubernetes deployment file for managing the application's replicas. The image tag inside the file is an environment variable which changes during the Jenkins pipeline according to the commit pushed from the repository.

### Service.yaml
Kubernetes service file for exposing the application within the cluster.

### Ingress.yaml
Kubernetes ingress file for routing external traffic to the application. It uses nginx's ingress (also included in this repository) and the EKS cluster's load balancer's DNS.

### Nginx-ingress-1.yml
Built-in yaml file for implementing Nginx ingress controller inside a kubernetes cluster so it is accessible to clients outside of the cluster.

