# Pub/Sub to Cloud Run Job

This project contains a Cloud Function that is triggered by a Pub/Sub message and then runs a Cloud Run job.

## Prerequisites

- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed.
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated.

## Usage

1.  **Create a `terraform.tfvars` file:**

    Create a file named `terraform.tfvars` in the root of the project and add the following content:

    ```
    project_id = "your-gcp-project-id"
    region     = "your-gcp-region"
    ```

2.  **Initialise Terraform:**

    ```
    terraform init
    ```

3.  **Plan and apply the changes:**

    ```
    terraform plan
    terraform apply
    ```

4.  **Trigger the function:**

    Publish a message to the `my-topic` Pub/Sub topic. The message should be a JSON string. You can do this from the Google Cloud Console or using the `gcloud` CLI:

    ```
    gcloud pubsub topics publish my-topic --message '{"key": "value"}'
    ```

## Testing

### Python

To run the tests for the python function, navigate to the `cloud_function` directory and run the following commands:

```
python3 -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt -r tests/requirements.txt
python -m unittest discover tests
```

### Go

To run the tests for the Go function, navigate to the `cloud_function_go/src` directory and run the following command:

```
go test
```
