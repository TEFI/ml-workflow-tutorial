variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "credentials_path" {
  type    = string
}

variable "machine_type" {
  type    = string
  default = "e2-medium"
}

# Name of the GKE cluster used for model serving
variable "serving_cluster_name" {
  description = "Name of the GKE cluster for serving models"
  type        = string
  default     = "ml-serving-cluster"
}

# Name of the GKE cluster used for model training
variable "training_cluster_name" {
  description = "Name of the GKE cluster for training models"
  type        = string
  default     = "ml-training-cluster"
}

# Variables required for deploying and managing resources in a Kubernetes (GKE) cluster

variable "bucket_name" {
  description = "Name of the GCS bucket"
  type        = string
  default = "ml-artifacts-tutorial"
}

variable "gcp_key_json_content" {
  description = "Base64-encoded content of the GCP service account key JSON file."
  type        = string
  sensitive   = true
}

variable "mlflow_db_password" {
  description = "Password for the MLflow database user"
  type        = string
  sensitive   = true
}