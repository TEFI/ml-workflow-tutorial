# Cloud SQL instance for MLflow metadata storage
resource "google_sql_database_instance" "mlflow" {
  name             = "mlflow-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    # Machine type (f1-micro is suitable for testing; use higher tiers for production)
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled = true

      # Allow access from any IP (only for testing; restrict in production)
      authorized_networks {
        name  = "allow-all"
        value = "0.0.0.0/0"
      }
    }

    # Enable automatic backups
    backup_configuration {
      enabled = true
    }
  }

  # Allow deletion without additional confirmation
  deletion_protection = false
}

# Create MLflow database inside the instance
resource "google_sql_database" "mlflow_db" {
  name     = "mlflow_db"
  instance = google_sql_database_instance.mlflow.name
}

# Create user for MLflow to connect to the database
resource "google_sql_user" "mlflow_user" {
  name     = "mlflow_user"
  instance = google_sql_database_instance.mlflow.name
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

