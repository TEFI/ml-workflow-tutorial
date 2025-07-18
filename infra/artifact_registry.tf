resource "google_artifact_registry_repository" "serving" {
  location      = var.region
  repository_id = "serving"
  format        = "DOCKER"
  description   = "Docker images for model serving"
}

resource "google_artifact_registry_repository" "trainer" {
  location      = var.region
  repository_id = "trainer"
  format        = "DOCKER"
  description   = "Docker images for model training jobs"
}

resource "google_artifact_registry_repository" "trainer_api" {
  location      = var.region
  repository_id = "trainer-api"
  format        = "DOCKER"
  description   = "Docker images for training API service that launches jobs"
}

resource "google_artifact_registry_repository" "monitor" {
  location      = var.region
  repository_id = "monitor"
  format        = "DOCKER"
  description   = "Docker images for monitoring services"
}

resource "google_artifact_registry_repository" "mlflowserver" {
  location     = var.region
  repository_id = "mlflowserver"
  description  = "Docker repository for custom MLflow server image"
  format       = "DOCKER"
}
