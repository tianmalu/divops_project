# divops_project
devops tarot for divination or fortune-telling

## 📁 Project Structure

```text
divops-tarot/
├── backend/                  # Spring Boot backend service
│   ├── src/
│   ├── Dockerfile
│   └── pom.xml
├── frontend/                 # Frontend app built with React or Angular
│   ├── public/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── ai-service/               # AI logic using Python and LangChain
│   ├── app/
│   │   ├── rag_engine.py
│   │   ├── tarot_prompt_template.txt
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── vector-db/                # Vector database config (e.g., Weaviate)
│   ├── docker-compose.yml
│   └── schema.json
├── k8s/                      # Kubernetes deployment manifests
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── ai-service-deployment.yaml
│   ├── weaviate-deployment.yaml
│   └── ingress.yaml
├── .github/                  # GitHub Actions workflows (CI/CD)
│   └── workflows/
│       └── ci-cd.yml
├── monitoring/               # Prometheus + Grafana monitoring setup
│   ├── prometheus.yml
│   ├── grafana/
│   └── docker-compose.yml
├── docs/                     # Project documentation and diagrams
│   ├── architecture.png
│   └── README.md
├── .gitignore                # Git ignore rules
├── docker-compose.yml        # Local dev integration entry point
└── README.md                 # Main project readme