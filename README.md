# 🧠 ML Workflow Tutorial

This is a simple **end-to-end machine learning pipeline** designed as a tutorial. It covers the full ML lifecycle including data preparation, model training, deployment, and evaluation.

## 📁 Project Structure

```
ml-workflow-tutorial/
│
├── .github/                # GitHub actions or issue templates
├── .vscode/                # Editor settings
├── infra/                  # Infrastructure as code (e.g., Terraform, GCP)
├── k8s/                    # Kubernetes manifests
├── ml_pipeline/            # ML pipeline components (e.g., preprocessing, utils)
├── secrets/                # Secret files (e.g., credentials, keys) – not tracked
├── services/               # Microservices (e.g., model server, API gateway)
├── tests/                  # Unit and integration tests
├── training_service/       # Model training scripts and configurations
├── .env                    # Environment variables (not included in Git)
├── .gitignore              # Files and folders ignored by Git
└── docker-compose.yml      # Orchestrates multi-container setup
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ml-workflow-tutorial.git
cd ml-workflow-tutorial
```

### 2. Create a `.env` file

Set required variables like:

```env
PROJECT_ID=test-pager-464339-p2
REGION=us-central1
ZONE=us-central1-a
GOOGLE_APPLICATION_CREDENTIALS=/secrets/your-credentials.json
```

### 3. Build and launch with Docker Compose

```bash
docker-compose up --build
```

### 4. Access

- Model API: [http://localhost:8000](http://localhost:8000)
- Other services depend on port configuration in `docker-compose.yml`

## ⚙️ Features

- Modular architecture for maintainability
- GCP-ready with Terraform and Kubernetes
- Model training and serving separation
- Centralized `.env` and secrets handling
- Built-in support for LLM evaluation (via `deepeval`)
- Compatible with CI/CD and cloud deployment

## 🧰 Tech Stack

- **Python**, **FastAPI**, **scikit-learn** or **PyTorch**
- **Docker / Docker Compose**
- **Terraform** for infrastructure
- **Kubernetes** for deployment (optional)
- **MLflow** or custom tracking (optional)
- **BERTopic** for drift detection (optional)

## 📌 Roadmap

- [ ] Add MLflow integration
- [ ] Add monitoring dashboard
- [ ] Add sample dataset and model
- [ ] Add full test coverage

## 📝 License

MIT License
