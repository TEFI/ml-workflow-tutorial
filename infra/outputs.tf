output "serving_cluster_name" {
  value = google_container_cluster.serving.name
}

output "training_cluster_name" {
  value = google_container_cluster.training.name
}

output "gcs_bucket_name" {
  value = google_storage_bucket.ml_artifacts.name
}

output "artifact_registry_url" {
  value = "us-central1-docker.pkg.dev/${var.project_id}/ml-images"
}
