resource "google_sql_database_instance" "mlflow" {
  name             = "mlflow-db"
  database_version = "POSTGRES_15"
  region           = var.region
  project          = var.project_id 

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "allow-all"
        value = "0.0.0.0/0"  # WARNING: open to all IPs – only use for testing
      }
    }

    backup_configuration {
      enabled = true
    }
  }

  deletion_protection = false
}

resource "google_sql_database" "mlflow_db" {
  name     = "mlflow_db"
  instance = google_sql_database_instance.mlflow.name
  project  = var.project_id
}

resource "google_sql_user" "mlflow_user" {
  name     = "mlflow_user"
  instance = google_sql_database_instance.mlflow.name
  project  = var.project_id
  password = var.mlflow_db_password
}

output "mlflow_sql_instance_ip" {
  value = google_sql_database_instance.mlflow.public_ip_address
}

output "mlflow_connection_uri" {
  description = "Full PostgreSQL connection URI for MLflow"
  value       = "postgresql://mlflow_user:${var.mlflow_db_password}@${google_sql_database_instance.mlflow.public_ip_address}:5432/mlflow_db"
  sensitive   = true
}