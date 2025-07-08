resource "google_artifact_registry_repository" "serving_repo" {
  location      = var.region
  repository_id = "serving-repo"
  format        = "DOCKER"
  description   = "Repository for serving Docker images"
}

resource "google_artifact_registry_repository" "training_repo" {
  location      = var.region
  repository_id = "training-repo"
  format        = "DOCKER"
  description   = "Repository for training Docker images"
}

resource "google_artifact_registry_repository" "training_service_repo" {
  location      = var.region
  repository_id = "training-service-repo"
  format        = "DOCKER"
  description   = "Repository for training service images"
}

resource "google_artifact_registry_repository" "monitor_repo" {
  location      = var.region
  repository_id = "monitor-repo"
  format        = "DOCKER"
  description   = "Repository for monitoring service images"
}
