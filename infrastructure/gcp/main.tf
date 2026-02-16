module "bigquery" {
  source = "./bigquery"

  dataset_id  = var.raw_nyc_tlc_record_dataset
  region      = var.data_region
}

module "gcs" {
  source = "./cloud-storage"

  name    = var.data_lakehouse_raw_bucket
  region  = var.data_region
}
