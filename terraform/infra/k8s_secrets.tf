data "local_file" "gcp_key" {
  filename =  abspath("${path.module}/../../keys/terraform-deployer-key.json")
}

# Create a Kubernetes secret in the serving cluster containing the GCP service account key
resource "kubernetes_secret" "gcp_key_serving" {
  provider = kubernetes.serving

  metadata {
    name = "gcp-key-secret"
  }

  data = {
    "key.json" = data.local_file.gcp_key.content
  }

  type = "Opaque"
}


resource "kubernetes_secret" "gcp_bucket_serving" {
  provider = kubernetes.serving

  metadata {
    name = "gcp-secrets"
  }

  data = {
    bucket-name = var.bucket_name
  }

  type = "Opaque"
}



resource "kubernetes_secret" "gcp_key_training" {
  provider = kubernetes.training

  metadata {
    name = "gcp-key-secret"
  }

  data = {
    "key.json" = data.local_file.gcp_key.content
  }

  type = "Opaque"
}


resource "kubernetes_secret" "gcp_bucket_training" {
  provider = kubernetes.training

  metadata {
    name = "gcp-secrets"
  }

  data = {
    bucket-name = var.bucket_name
  }

  type = "Opaque"
}