variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "credentials_path" {
  type    = string
  default = "../keys/key.json"
}

variable "machine_type" {
  type    = string
  default = "e2-medium"
}

# Name of the GKE cluster used for model serving
variable "serving_cluster_name" {
  description = "Name of the GKE cluster for serving models"
  type        = string
  default     = "ml-serving-cluster"
}

# Name of the GKE cluster used for model training
variable "training_cluster_name" {
  description = "Name of the GKE cluster for training models"
  type        = string
  default     = "ml-training-cluster"
}

