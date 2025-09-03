
import base64
import json
import os

from google.cloud import run_v2

def handler(event, context):
    """
    Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    try:
        pubsub_message = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
    except json.JSONDecodeError:
        print("Error decoding JSON from Pub/Sub message")
        return

    print(f"Received message: {pubsub_message}")

    project = os.environ.get("GCP_PROJECT")
    region = os.environ.get("FUNCTION_REGION")
    job_name = os.environ.get("TARGET_CLOUD_RUN_JOB")

    if not all([project, region, job_name]):
        raise ValueError(
            "Missing required environment variables: GCP_PROJECT, FUNCTION_REGION, TARGET_CLOUD_RUN_JOB"
        )

    run_job(project, region, job_name, json.dumps(pubsub_message))


def run_job(project: str, region: str, job_name: str, message: str):
    """
    Creates and runs a Cloud Run job.
    Args:
        project: The Google Cloud project ID.
        region: The region where the Cloud Run job is located.
        job_name: The name of the Cloud Run job.
        message: The message to pass to the job as an argument.
    """
    client = run_v2.JobsClient()

    request = run_v2.RunJobRequest(
        name=f"projects/{project}/locations/{region}/jobs/{job_name}",
        overrides=run_v2.RunJobRequest.Overrides(
            container_overrides=[
                run_v2.RunJobRequest.Overrides.ContainerOverride(
                    args=[message],
                ),
            ],
        ),
    )

    operation = client.run_job(request=request)
    print(f"Started Cloud Run job: {operation.metadata.name}")
    return operation
