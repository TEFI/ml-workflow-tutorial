provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
  credentials = file("gcp-key.json")
}

resource "google_compute_network" "vpc" {
  name = "ml-vpc"
}

resource "google_compute_firewall" "allow-http-mlflow" {
  name    = "allow-http-ssh-mlflow"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "5000", "8000", "9090"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "ml_vm" {
  name         = "mlflow-monitoring-vm"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = google_compute_network.vpc.name
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io docker-compose git
    systemctl start docker
    systemctl enable docker
    git clone https://github.com/TEFI/ml-workflow-tutorial.git
    cd ml-workflow-tutorial
    echo "MODEL_PATH=/models/model.pkl" > .env
    mkdir -p secrets
    echo "fake-secret" > secrets/secret.txt
    docker compose up -d
  EOT

  tags = ["ml-server"]
}