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
}

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
  }
}
