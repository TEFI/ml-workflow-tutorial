# GKE training cluster
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

# Espera a que el cluster esté listo antes de usarlo como data source
data "google_container_cluster" "training" {
  name       = google_container_cluster.training.name
  location   = google_container_cluster.training.location
  depends_on = [google_container_cluster.training]
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

# Kubernetes provider for training cluster
provider "kubernetes" {
  alias                  = "training"
  host                   = "https://${data.google_container_cluster.training.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(data.google_container_cluster.training.master_auth[0].cluster_ca_certificate)
}

# GCP service account key secret in training cluster
resource "kubernetes_secret" "gcp_key" {
  provider = kubernetes.training

  metadata {
    name = "gcp-key-secret"
  }

  data = {
    "key.json" = base64encode(var.gcp_key_json_content)
  }

  type = "Opaque"
}
