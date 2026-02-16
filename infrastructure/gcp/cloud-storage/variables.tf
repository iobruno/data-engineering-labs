variable "name" {
    type        = string
    description = "Bucket name"
}

variable "region" {
    type        = string
    description = "Region where the bucket should be created at"
}

variable "storage_class" {
  type        = string
  description = "Google Cloud Storage Storage Class"
  default     = "STANDARD"
}

variable "expires_in" {
  type        = number
  description = "Number of days in the object lifecycle before expiration"
  default     = 30
}
