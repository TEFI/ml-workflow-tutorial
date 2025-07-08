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

## 🔐 Creating a Terraform Service Account in GCP

To manage GCP infrastructure with Terraform, it's recommended to create a dedicated service account with the necessary permissions. Below are the steps to create one called `terraform-deployer`.

### 1. Create the Service Account

```bash
gcloud iam service-accounts create terraform-deployer \
  --description="Service account for Terraform deployments" \
  --display-name="Terraform Deployer"
```

### 2. Assign Required IAM Roles

Replace `PROJECT_ID` with your actual GCP project ID. If you're using PowerShell, run each command separately.

```powershell
$SA_EMAIL="terraform-deployer@PROJECT_ID.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/iam.serviceAccountAdmin"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/container.admin"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/artifactregistry.admin"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/logging.logWriter"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/monitoring.metricWriter"
```

> 💡 Make sure your user has Owner or IAM Admin permissions to assign roles.

### 3. Create a JSON Key

This will generate a credentials file for Terraform to authenticate with GCP.

```bash
gcloud iam service-accounts keys create terraform-deployer-key.json \
  --iam-account=terraform-deployer@PROJECT_ID.iam.gserviceaccount.com
```

Store the resulting `terraform-deployer-key.json` file securely.

### 4. Use the Key in Terraform

In your Terraform provider block, use the generated key:

```hcl
provider "google" {
  credentials = file("terraform-deployer-key.json")
  project     = "PROJECT_ID"
  region      = "us-central1"
}
```

Now Terraform is ready to deploy resources using your new service account.


## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ml-workflow-tutorial.git
cd ml-workflow-tutorial
```

### 2. Create a `.env` file

Set required variables like:

```env
PROJECT_ID=test-pager-464339-p
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
