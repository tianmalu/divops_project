# Team DivOps Server

This repository contains the backend services for the TarotAI platform, implemented as two independent Spring Boot microservices:

- **Discussions Service** (`server/discussions`)
- **Users Service** (`server/users`)

Each service is containerized and can be run locally for development or deployed to production using Docker, Kubernetes, or AWS.

---

## Project Overview

- **Framework:** Java 17, Spring Boot 3
- **Database:** PostgreSQL (with Flyway migrations)
- **Security:** JWT-based authentication
- **API Docs:** OpenAPI/Swagger (auto-generated)
- **Build Tool:** Gradle

### Services

#### Discussions Service

- Manages tarot card discussions and questions.
- Integrates with the GenAI service for tarot card responses.
- REST API endpoints for creating discussions, posting questions, and retrieving discussion details.

#### Users Service

- Handles user registration, authentication, and user management.
- Provides JWT tokens for secure API access.
- REST API endpoints for user login, registration, and profile management.

---

## How It Works

- Each service is a standalone Spring Boot application.
- Services connect to their own PostgreSQL databases.
- JWT tokens are used for authentication and authorization.
- Database migrations are managed with Flyway.
- OpenAPI documentation is available at `/swagger-ui/index.html` when running.

---

## Development Setup

### Prerequisites

- Java 17+
- Gradle
- Docker (for containerized development)
- PostgreSQL (or use Docker Compose for local DB)

### Environment Configuration

Each service uses an `application.properties` file for configuration. Example (Discussions):

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/discussions_db
spring.datasource.username=discussions_db_username
spring.datasource.password=discussions_db_password
spring.jpa.hibernate.ddl-auto=validate
```

**Tip:** You can override these with environment variables or by mounting a custom properties file.

---

### Running in Development Mode

#### Using Gradle (local)

```bash
# Discussions Service
cd server/discussions
./gradlew bootRun

# Users Service
cd server/users
./gradlew bootRun
```

#### Using Docker

Each service has a development Dockerfile:

```bash
# Discussions Service
cd server/discussions
docker build -f Dockerfile.dev -t discussions-dev .
docker run -p 8080:8080 --env-file .env discussions-dev

# Users Service
cd server/users
docker build -f Dockerfile.dev -t users-dev .
docker run -p 8080:8080 --env-file .env users-dev
```

---

## Building for Production

```bash
# Discussions Service
cd server/discussions
./gradlew build

# Users Service
cd server/users
./gradlew build
```

- The JAR will be in `build/libs/`.

---

## Deployment

### Docker (Production)

Each service has a production Dockerfile:

```bash
# Discussions Service
cd server/discussions
docker build -f Dockerfile.prod -t discussions .
docker run -p 8080:8080 --env-file .env discussions

# Users Service
cd server/users
docker build -f Dockerfile.prod -t users .
docker run -p 8080:8080 --env-file .env users
```

### Kubernetes (Helm)

Helm charts are available under `helm/divops/` for deploying both services to Kubernetes.

### AWS (Terraform/Ansible)

- To deploy to AWS, set the `RUN_AWS_DEPLOYMENT` variable in GitHub Actions to `true`.
- Update the following secrets in your repository:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_SESSION_TOKEN`
  - `AWS_EC2_SSH_PRIVATE_KEY`
- The pipeline will provision infrastructure and deploy the services.

---

## Environment Variables

Each service expects the following (see `application.properties` for full list):

- `spring.datasource.url`
- `spring.datasource.username`
- `spring.datasource.password`
- (and others as needed for your environment)

---

## Linting & Testing

- **Linting:** Standard Java linting via IDE or CI pipeline.
- **Testing:** JUnit tests are included. To run:

```bash
./gradlew test
```

---

## API Documentation

- Swagger UI is available at: `http://localhost:8080/swagger-ui/index.html` (when running).
