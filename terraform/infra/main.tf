# Configure the Google Cloud provider with project, region, zone and credentials
provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = var.zone
  credentials = file(var.credentials_path)
}

# Enable GKE (Google Kubernetes Engine) API for creating and managing Kubernetes clusters
resource "google_project_service" "gke" {
  project = var.project_id
  service = "container.googleapis.com"
}


# Enable Cloud Run API (used for deploying and running containerized services)
resource "google_project_service" "cloud_run" {
  service = "run.googleapis.com"
  project = var.project_id
}

# Enable Cloud SQL Admin API (required for managing Cloud SQL instances)
resource "google_project_service" "cloudsql_admin" {
  project = var.project_id
  service = "sqladmin.googleapis.com"
}

# Access information about the currently configured Google Cloud client
data "google_client_config" "default" {}
