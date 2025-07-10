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

# Core IAM permissions
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/iam.serviceAccountAdmin"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/resourcemanager.projectIamAdmin"

# GKE and Artifact Registry
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/container.admin"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/artifactregistry.admin"

# Compute Engine and Networking
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/compute.instanceAdmin.v1"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/compute.networkAdmin"

# Storage, Logging, Monitoring
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/storage.admin"
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


# 🔐 Setting up GitHub Secrets for CI/CD

This guide explains how to configure the required GitHub secrets for the CI/CD pipeline defined in `.github/workflows/ci-cd.yaml`.

GitHub Actions uses encrypted secrets to manage sensitive information (e.g., credentials, project IDs, cluster names). These secrets are injected into your workflow using `${{ secrets.<SECRET_NAME> }}`.

## ✅ Required Secrets

| Secret Name           | Description |
|------------------------|-------------|
| `GCP_KEY`             | The full content of your service account key in JSON format. |
| `GCP_PROJECT_ID`      | Your Google Cloud Project ID. |
| `TIME_ZONE_DOCKER`    | The region name used in your Artifact Registry URL (e.g., `us-central1`). |
| `TIME_ZONE_GKE`       | The zone of your GKE clusters (e.g., `us-central1-a`). |
| `SERVING_CLUSTER`     | Name of the GKE cluster for the `serving` deployment. |
| `TRAINING_CLUSTER`    | Name of the GKE cluster for the `training_service` deployment. |

## 🛠️ How to Add Secrets in GitHub

1. Go to your repository on GitHub.
2. Click on **Settings**.
3. In the sidebar, select **Secrets and variables > Actions**.
4. Click **New repository secret**.
5. Enter the **name** and **value** of the secret.
6. Click **Add secret**.

Repeat this process for each of the required secrets listed above.

## 🔐 Example: Creating `GCP_KEY` Secret

If you have a JSON key file for your service account (e.g., `terraform-deployer.json`), you can create the secret with:

```bash
gh secret set GCP_KEY < terraform-deployer.json
```

Or paste its content directly when adding it manually in the GitHub UI.

## 📦 Artifact Registry URL Format

The `TIME_ZONE_DOCKER` secret should match the region of your Artifact Registry and is used to form the URL:

```
<TIME_ZONE_DOCKER>-docker.pkg.dev/<GCP_PROJECT_ID>/<REPO_NAME>/<IMAGE_NAME>
```

Example:
```
us-central1-docker.pkg.dev/sodium-pager-461309-p3/serving-repo/serving-api
```

## 🧠 Pro Tip

Avoid hardcoding secrets or sensitive values directly in your workflow files. Always use `${{ secrets.NAME }}` to keep your credentials safe.

---

Once your secrets are configured, your CI/CD pipeline will be able to:
- Authenticate with Google Cloud
- Build and push Docker images
- Deploy to the correct GKE cluster

Happy deploying 🚀


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
