resource "google_storage_bucket" "ml_artifacts" {
  name     = "ml-artifacts-tutorial"
  location = var.region
  force_destroy = true
}
