
resource "google_cloud_run_v2_job" "default" {
  name     = "my-job"
  location = var.region

  template {
    template {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/job:latest"
      }
    }
  }
}
