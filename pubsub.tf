
resource "google_pubsub_topic" "default" {
  name = "my-topic"
}

resource "google_cloudfunctions2_function" "default" {
  name     = "my-function"
  location = var.region

  build_config {
    runtime     = "python313"
    entry_point = "handler"
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.default.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    service_account_email = google_service_account.default.email
    environment_variables = {
      "TARGET_CLOUD_RUN_JOB" = google_cloud_run_v2_job.default.name
      "GCP_PROJECT"          = var.project_id
      "FUNCTION_REGION"      = var.region
    }
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.default.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

resource "google_service_account" "default" {
  account_id   = "my-function-sa"
  display_name = "My Function Service Account"
}

resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.jobsExecutorWithOverrides"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_storage_bucket" "default" {
  name                        = "${var.project_id}-cf-source"
  location                    = var.region
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "default" {
  name   = "source.zip"
  bucket = google_storage_bucket.default.name
  source = "cloud_function.zip"
}
