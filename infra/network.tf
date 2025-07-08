resource "google_compute_network" "gke_vpc" {
  name                    = "gke-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "gke_subnet" {
  name          = "gke-subnet"
  ip_cidr_range = "10.10.0.0/16"
  region        = var.region
  network       = google_compute_network.gke_vpc.id
}

resource "google_compute_router" "gke_router" {
  name    = "gke-router"
  network = google_compute_network.gke_vpc.id
  region  = var.region
}

resource "google_compute_router_nat" "gke_nat" {
  name                               = "gke-nat"
  router                             = google_compute_router.gke_router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ALL"
  }
}
