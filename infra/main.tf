
provider "google" {
  project     = var.project_id
  region      = var.region
  zone    = var.zone
  credentials = file(var.credentials_path)
}

resource "google_project_service" "cloud_run" {
  service = "run.googleapis.com"
  project = var.project_id
}
