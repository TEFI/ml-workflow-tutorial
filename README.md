# 🧠 ML Workflow Tutorial

This project provides a minimal yet complete **end-to-end machine learning pipeline** built as a learning and reference tool. It demonstrates the full ML lifecycle: data preprocessing, training, deployment, tracking, and serving — all powered by modern tools like **Terraform**, **Kubernetes**, **MLflow**, and **FastAPI**.

---

## 📁 Project Structure

```
ml-workflow-tutorial/
├── .github/workflows/         # GitHub Actions for CI/CD
├── .vscode/                   # VSCode settings (not versioned)
├── terraform/infra/           # Infrastructure-as-Code (Terraform for GCP)
├── k8s/                       # Kubernetes manifests
├── ml_pipeline/               # ML pipeline logic (preprocessing, training utils)
├── keys/                      # Local secrets (e.g., GCP service account key) – not versioned
├── services/                  # Microservices (MLflow, model server, training jobs)
│   ├── mlflow/
│   ├── model-server/
│   └── training/
├── .env                       # Environment variables
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ml-workflow-tutorial.git
cd ml-workflow-tutorial
```

### 2. Create your `.env` file

```env
PROJECT_ID=your-gcp-project-id
REGION=us-central1
ZONE=us-central1-a
GOOGLE_APPLICATION_CREDENTIALS=/keys/terraform-deployer-key.json
```

---

## ☁️ Provision Infrastructure with Terraform

### 1. Create a GCP Service Account

```bash
gcloud iam service-accounts create terraform-deployer   --description="Terraform service account"   --display-name="Terraform Deployer"
```

### 2. Assign IAM Roles

Assign roles needed for Terraform, GKE, Cloud Run, Artifact Registry, Storage, Logging, etc.:

```bash
SA_EMAIL="terraform-deployer@your-project-id.iam.gserviceaccount.com"
PROJECT_ID="your-project-id"

gcloud projects add-iam-policy-binding $PROJECT_ID   --member="serviceAccount:$SA_EMAIL"   --role="roles/iam.serviceAccountAdmin"
```

### 3. Generate Service Account Key

```bash
gcloud iam service-accounts keys create terraform-deployer-key.json   --iam-account=$SA_EMAIL
```

### 4. Use the key in Terraform

```hcl
provider "google" {
  credentials = file("terraform-deployer-key.json")
  project     = "your-project-id"
  region      = "us-central1"
}
```

---

## 🔐 CI/CD: GitHub Secrets

Set the following GitHub Action secret:

| Secret Name | Description |
|-------------|-------------|
| `GCP_KEY`   | Base64-encoded JSON of your GCP service account key |

To add it:

```bash
gh secret set GCP_KEY < terraform-deployer-key.json
```

---

## 🛠️ Running Terraform

1. Navigate to the Terraform folder:

```bash
cd terraform/infra
```

2. Fill in your variables in `terraform.tfvars`.

Example:
  project_id = "sodium-pager-461309-p3"
  region     = "us-central1"
  zone       = "us-central1-a"
  credentials_path = "/keys/terraform-deployer-key.json"
  machine_type     = "e2-medium"
  bucket_name = "ml-artifacts-tutorial"
  mlflow_db_password = "mlflow123"

3. Initialize and apply:

```bash
terraform init
terraform apply
```
> 🔐 Note: You will be prompted to enter your GCP key in **Base64 format** during the Terraform process. You can convert it using:
>
> ```powershell
> [Convert]::ToBase64String([IO.File]::ReadAllBytes("C:/path/to/terraform-deployer-key.json"))
> ```
---

## 📦 Deploy to Production

1. **Configure GitHub CI/CD environment variables**

   Edit your GitHub Actions workflow and set the following environment variables:

   ```yaml
   env:
     GCP_PROJECT_ID: your-project-id
     GCP_REGION: us-central1
     GCP_ZONE: us-central1-a
     SERVING_CLUSTER: ml-serving-cluster
     TRAINING_CLUSTER: ml-training-cluster
   ```

2. **Deploy MLflow (manually or via CI/CD)**

   You can deploy MLflow in two ways:

   - **Manual deployment** using `kubectl`:

     ```bash
     kubectl apply -f k8s/deployment_mlflow.yaml
     kubectl apply -f k8s/service_mlflow.yaml
     ```

   - **CI/CD deployment**: trigger the GitHub Actions pipeline by pushing any change (e.g., a newline) to the repo.

   Once deployed, run:

   ```bash
   kubectl get svc
   ```

   Look for the `EXTERNAL-IP` of `mlflow-service`. Example output:

   ```
   NAME             TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)
   mlflow-service   LoadBalancer   34.118.230.108  146.148.62.66    5000:31703/TCP
   ```

3. **Update config variables in scripts**

   In `ml_pipeline/config.py`:

   ```python
   MLFLOW_URI = os.getenv("MLFLOW_URI", "http://146.148.62.66:5000")
   EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "random-forest-classifier")
   ```

   In `services/training/app/config.py`:

   ```python
   PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
   REGION = os.getenv("REGION", "us-central1")
   BUCKET_NAME = os.getenv("BUCKET_NAME", "ml-artifacts-tutorial")
   SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT", "terraform-deployer@your-project-id.iam.gserviceaccount.com")
   IMAGE_URI = os.getenv("IMAGE_URI", "us-central1-docker.pkg.dev/your-project-id/trainer/training-job:latest")
   ```

4. **Trigger a model training job**

   Train a model using the Titanic dataset. You can get it from Kaggle or a public URL. The job will be executed using Cloud Run Jobs and visible at:

   [https://console.cloud.google.com/run/jobs](https://console.cloud.google.com/run/jobs)

   Once trained, the model will be logged in MLflow automatically.

5. **Deploy the model server**

   Configure `services/model-server/app/config.py`:

   ```python
   MLFLOW_URI = os.getenv("MLFLOW_URI", "http://146.148.62.66:5000")
   MODEL_URI = os.getenv("MODEL_URI", "models:/RandomForestModelv1@production")
   ```

   Get credentials for the serving cluster and deploy:

   ```bash
   gcloud container clusters get-credentials ml-serving-cluster --zone=us-central1-a
   kubectl apply -f k8s/model_server.yaml
   ```

   Then, retrieve the external IP of the model server:

   ```bash
   kubectl get svc
   ```

   Example output:

   ```
   NAME          TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)
   serving-api   LoadBalancer   34.118.226.97    34.9.240.78     80:31902/TCP
   ```

6. **Make predictions via HTTP**

   You can now make inference requests using `curl` or Postman:

   ```bash
   curl -X POST http://34.9.240.78/predict      -H "Content-Type: application/json"      -d '{
       "Pclass": 1,
       "Sex": "female",
       "Age": 22,
       "SibSp": 1,
       "Parch": 0,
       "Fare": 7.25,
       "Embarked": "S"
     }'
   ```

---




---

## ⚙️ Features

- Modular and production-ready ML architecture
- Full ML lifecycle from training to serving
- IaC with Terraform for reproducible infra
- ML tracking with MLflow
- Real-time serving with FastAPI
- Compatible with GitHub CI/CD

---

## 🧰 Tech Stack

- **Python**, **FastAPI**, **scikit-learn**
- **Terraform** for cloud provisioning
- **Kubernetes** for orchestration
- **MLflow** for experiment tracking
- **Google Cloud Platform**

---

## 📌 Roadmap

- [ ] Add Prometheus/Grafana monitoring
- [ ] Add automated tests and test coverage
- [ ] Add multi-model support
- [ ] Add feature store integration

---

## 📝 License

MIT License
