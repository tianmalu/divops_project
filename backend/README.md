# Backend Deployment Guide

This backend project is built with Spring Boot and Docker. Follow the steps below to build, run, and test the application.

## 1. Build the Backend Jar

Run the following command to generate the `.jar` file:

```
mvn clean package
```

## 2. Build the Docker Image
Navigate to the backend/ folder and build the Docker image:
```
docker build -t my-backend:latest .
```

## 3. Run the Docker Container
Start the container with the following command:
```
docker run -d -p 8080:8080 --name backend-container my-backend:latest
```

## 4. Verify the Service
Use curl to check if the backend API is running properly:
```
curl "http://localhost:8080/api/predict?question=Will%20I%20be%20rich"
```