# TarotAI Client

This is the frontend client for the TarotAI platform, built with **React**, **TypeScript**, and **Vite**. It provides a modern, responsive user interface for authentication, tarot card discussions, and user feeds, communicating with backend services via REST APIs.

## Project Overview

- **Framework:** React 19 + Vite
- **UI Library:** Mantine
- **API Integration:** OpenAPI-generated clients for seamless backend communication
- **Features:**
  - User authentication (login/signup)
  - Tarot card discussions and feeds
  - Protected routes for authenticated users
  - Responsive, dark-themed UI

## How It Works

- The app uses React Router for navigation and Mantine for UI components and theming.
- API requests are handled via OpenAPI clients, with JWT-based authentication.
- The main pages include:
  - **Login/Signup:** User authentication
  - **User Dashboard:** Access to tarot discussions and feed
  - **Discussions:** Start and follow tarot card discussions
  - **Feed:** Infinite scrolling feed of posts/discussions


To start developing, create `.env.development` file and make sure it contains

- The app will be available at [http://localhost:3000](http://localhost:3000).
- By default, it expects backend services to be running and accessible via environment variables.


#### Development

A development Dockerfile and .env is provided:

```bash
docker build -f Dockerfile.dev -t tarotai-client-dev .
docker run -p 3000:3000 tarotai-client-dev
```

#### Production

A production-ready image serves the built app via Nginx:

```bash
docker build -f Dockerfile.prod -t tarotai-client .
docker run -p 80:80 tarotai-client
```

### Kubernetes (Helm)

A Helm chart is available under `helm/divops/client/` for deploying to Kubernetes:

```bash
cd helm/divops
helm install client ./client
```

- See `helm/divops/client/values.yaml` for configuration options.

### AWS (Terraform/Ansible)

To deploy to AWS, set the `RUN_AWS_DEPLOYMENT` in the Github variables to `true` to make the job required for the deployment to work. This flag was implemented as the tokens and access keys change in the lab. Then, in the secrets, update these values with your account's info

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`

Then, in the AWS EC2, create a key pair and name it `ec2`. Download the private key from AWS and add it in this secret

- `AWS_EC2_SSH_PRIVATE_KEY`

Run the pipeline and it will deploy the client to a newly created instance and print its ip address


## Environment Variables

The client expects the following environment variables (typically set via `.env`):

- `VITE_USERS_SERVICE_API_BASE_URL`
- `VITE_DISCUSSIONS_SERVICE_API_BASE_URL`


### Linting

Linting is done used `biome.js`
It is also in the CI/CD pipeline

To run, use the configured command: `npm run lint`


###  Testing

Testing is done using vitest and all necessary setup is configured

To run, use: `npm test`

