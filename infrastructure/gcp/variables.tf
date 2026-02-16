variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "data_region" {
  type        = string
  description = "Region for GCP Resources"
  default     = "us-central1"
}

variable "data_lakehouse_raw_bucket" {
  type        = string
  description = "Bucket name for the raw layer of the Data Lakehouse"
}

variable "raw_nyc_tlc_record_dataset" {
  type        = string
  description = "BigQuery Dataset for the raw data from NYC trip record data"
}

