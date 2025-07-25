# GKE cluster for model serving
resource "google_container_cluster" "serving" {
  name     = var.serving_cluster_name
  location = var.zone
  network  = "default"  # Using the default VPC network

  remove_default_node_pool = true  # We'll create a custom node pool below
  initial_node_count       = 1     # Required by GCP even if we remove the default pool
  deletion_protection      = false # Allows the cluster to be destroyed via Terraform

  ip_allocation_policy {
    stack_type = "IPV4"
  }

  # Ensure GKE API is enabled before creating the cluster
  depends_on = [google_project_service.gke]
}

# Wait until the cluster is ready before using it as a data source
data "google_container_cluster" "serving" {
  name       = google_container_cluster.serving.name
  location   = google_container_cluster.serving.location

  # Make sure the cluster exists before trying to query it
  depends_on = [google_container_cluster.serving]
}

# Custom node pool for the serving cluster
resource "google_container_node_pool" "serving_nodes" {
  name       = "serving-node-pool"
  cluster    = google_container_cluster.serving.name
  location   = var.zone
  node_count = 1

  node_config {
    machine_type    = "e2-medium"                        # VM type for the nodes
    disk_size_gb    = 50                                 # Disk size per node
    disk_type       = "pd-standard"                      # Standard persistent disk
    service_account = google_service_account.gke_sa.email # GCP service account used by the nodes
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"] # Full access to all GCP services
  }
}

# IAM binding: allow pulling from Artifact Registry for serving cluster too
resource "google_project_iam_member" "gke_sa_artifact_registry_serving" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}

# Kubernetes provider configuration for the serving cluster
provider "kubernetes" {
  alias                  = "serving"
  host                   = "https://${data.google_container_cluster.serving.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(data.google_container_cluster.serving.master_auth[0].cluster_ca_certificate)
}

