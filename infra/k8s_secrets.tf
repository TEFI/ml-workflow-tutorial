resource "kubernetes_secret" "gcp_secrets_training" {
  provider = kubernetes.training

  metadata {
    name = "gcp-secrets"
  }

  data = {
    bucket-name = var.bucket_name
    blob-name   = var.blob_name
  }

  type = "Opaque"
}

resource "kubernetes_secret" "gcp_secrets_serving" {
  provider = kubernetes.serving

  metadata {
    name = "gcp-secrets"
  }

  data = {
    bucket-name = var.bucket_name
    blob-name   = var.blob_name
  }

  type = "Opaque"
}
