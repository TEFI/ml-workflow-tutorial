# GKE training cluster definition
resource "google_container_cluster" "training" {
  name     = var.training_cluster_name
  location = var.zone
  network  = "default"

  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false

  ip_allocation_policy {
    stack_type = "IPV4"
  }
  depends_on = [google_project_service.gke]
}

# Data source to fetch training cluster details after creation
data "google_container_cluster" "training" {
  name       = google_container_cluster.training.name
  location   = google_container_cluster.training.location
  depends_on = [google_container_cluster.training]
}

# Node pool with node-role=training label
resource "google_container_node_pool" "training_nodes" {
  name       = "training-node-pool"
  cluster    = google_container_cluster.training.name
  location   = var.zone
  node_count = 1

  node_config {
    machine_type    = "e2-medium"
    disk_size_gb    = 50
    disk_type       = "pd-standard"
    service_account = google_service_account.gke_sa.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    labels = {
      node-role = "training"
    }
  }
}

# Kubernetes provider configured for training cluster
provider "kubernetes" {
  alias                  = "training"
  host                   = "https://${data.google_container_cluster.training.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(data.google_container_cluster.training.master_auth[0].cluster_ca_certificate)
}

