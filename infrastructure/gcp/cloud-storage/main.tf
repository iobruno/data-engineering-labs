resource "google_storage_bucket" "this" {
  name      = var.name
  location  = var.region

  # Cascade delete all objects within when the bucket is deleted
  force_destroy               = true
  uniform_bucket_level_access = true
  storage_class               = var.storage_class

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = var.expires_in
    }
    action {
      type = "Delete"
    }
  }
}
