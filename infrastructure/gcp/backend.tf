terraform {
    backend "gcs" {
        bucket  = "iobruno-gcp-labs-tfstate"
    }
}
