resource "google_storage_bucket" "ml_artifacts" {
  name          = var.bucket_name             # Bucket name (must be globally unique)
  location      = var.region                  # Region (e.g., "us-central1")
  force_destroy = true                        # Allow deletion even if bucket has objects
  storage_class = "STANDARD"                  # Optional: could also be NEARLINE, COLDLINE, etc.
}
